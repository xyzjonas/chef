import pytest
from sqlalchemy.orm import Session

from chef.api.common import generic_get
from chef.controllers import RecipesController
from chef.models import Recipe, Ingredient, Tag, Unit
from chef.schemas import Recipe as RecipeSchema

R1 = {
    "ingredients": [
        {"amount": "100", "unit": {"name": "g"}, "ingredient": {"name": "rice"}}
    ],
    "tags": [
        {"name": "tag"}
    ],
    "title": "Test",
    "subtitle": "subtitle",
    "portions": 20,
    "source": "source",
    "source_name": "source_name",
    "body": "body",
    "draft": True,
    "favorite": True,
}

R2 = {
    "ingredients": [
        {"amount": "300", "unit": {"name": "ml"}, "ingredient": {"name": "rice"}},
        {"amount": "1", "unit": {"name": "kg"}, "ingredient": {"name": "pork"}},
    ],
    "tags": [
        {"name": "tag"},
        {"name": "tag2"}
    ],
    "title": "Test #2",
    "subtitle": "let's see if tags/ingredients don't get duplicated",
    "portions": 1,
    "source": "source",
    "source_name": "http://source/path#fragment?query=True",
    "body": "body",
    "draft": False,
    "favorite": False,
}


def _assert_recipe_matches(session: Session, recipe: dict):
    actual_recipe = session.query(Recipe).filter_by(title=recipe["title"]).first()
    assert actual_recipe
    for attr in (
            "title", "subtitle", "source",
            "source_name", "body", "portions", "draft", "favorite"
    ):
        assert getattr(actual_recipe, attr) == recipe[attr]

    actual_ingredient_items = getattr(actual_recipe, "ingredients", [])
    assert len(actual_ingredient_items) == len(recipe.get("ingredients") or [])
    for actual_item, ingredient in zip(actual_ingredient_items, recipe["ingredients"]):
        assert actual_item.amount == float(ingredient["amount"])
        actual_ingredient_unit = actual_item.unit.get_dictionary(exclude="id")
        assert actual_ingredient_unit == {
            "name": ingredient["unit"]["name"],
            "grams": ingredient["unit"].get("grams", 0),
        }
        actual_ingredient = actual_item.ingredient.dictionary
        del actual_ingredient["id"]
        assert actual_ingredient == {
            'name': ingredient["ingredient"]["name"],
            'carbs': ingredient["ingredient"].get("carbs", 0),
            'density': ingredient["ingredient"].get("density", 1000),
            'energy': ingredient["ingredient"].get("energy", 0),
            'fats': ingredient["ingredient"].get("fats", 0),
            'fibres': ingredient["ingredient"].get("fibres", 0),
            'is_liquid': ingredient["ingredient"].get("is_liquid", 0),
            'proteins': ingredient["ingredient"].get("proteins", 0),
            'salt': ingredient["ingredient"].get("salt", 0)
        }

    actual_tags = getattr(actual_recipe, "tags", [])
    assert len(actual_tags) == len(recipe.get("tags", []))
    for actual_tag, expected_tag in zip(actual_tags, recipe.get("tags", [])):
        assert actual_tag.get_dictionary(exclude=["id"]) == expected_tag


def test_get_recipes(http_client, simple_test_data):
    recipe, ii, i, t = simple_test_data

    response = http_client.get("/api/recipes")
    assert response.status_code == 200
    assert type(response.json()) is list
    assert len(response.json()) == 1
    assert response.json()[0] == RecipeSchema(**recipe.dictionary)


def test_add_recipe_minimal(db_session, http_client):
    response = http_client.post("/api/recipes", json={"title": "spaghetti"})
    assert response.status_code == 201
    assert db_session.query(Recipe).filter_by(title="spaghetti").first()


@pytest.mark.parametrize("data", [
    {},
    {"title": None},
])
def test_add_recipe_invalid_type(db, http_client, data):
    response = http_client.post("/api/recipes", json=data)
    assert response.status_code == 422


@pytest.mark.parametrize("data", [
    [R1],
    [R1, R2],
    [R2, R1]
])
def test_add_recipe(db_session, http_client, data: dict):

    for recipe in data:
        response = http_client.post("/api/recipes", json=recipe)
        response.raise_for_status()
        assert response.status_code == 201

    for recipe in data:
        _assert_recipe_matches(db_session, recipe)


@pytest.mark.parametrize("first_unit", [None, {"name": "g"}], ids=["none", "g"])
def test_create_recipe_no_unit(db_session, http_client, first_unit):
    data = {
        "ingredients": [
            {"amount": "100", "ingredient": {"name": "rice"}}
        ],
        "title": "Test",
    }
    if first_unit:
        data["ingredients"][0]["unit"] = first_unit

    response = http_client.post("/api/recipes", json=data)
    assert response.status_code == 201

    r = db_session.query(Recipe).filter_by(title=data["title"]).first()
    assert r
    assert r.title == data["title"]
    assert len(r.ingredients) == 1
    assert r.ingredients[0].ingredient.name == data["ingredients"][0]["ingredient"]["name"]
    assert r.ingredients[0].unit.name == data["ingredients"][0]["unit"]["name"] \
        if first_unit else "pcs"

    if data["ingredients"][0].get("unit"):
        del data["ingredients"][0]["unit"]
    response = http_client.put(f"/api/recipes/{r.id}", json=data)
    assert response.status_code == 200

    db_session.expire_all()
    r = db_session.query(Recipe).filter_by(title=data["title"]).first()
    assert r
    assert r.title == "Test"
    assert len(r.ingredients) == 1
    assert r.ingredients[0].ingredient.name == "rice"
    assert r.ingredients[0].unit.name == "pcs"


def test_edit_recipe(db_session, http_client):
    response = http_client.post("/api/recipes", json=R1)
    response.raise_for_status()
    recipe_id = response.json()["id"]
    _assert_recipe_matches(db_session, R1)

    response = http_client.put(f"/api/recipes/{recipe_id}", json=R2)
    response.raise_for_status()
    assert response.json()["id"] == recipe_id
    _assert_recipe_matches(db_session, R2)


def test_delete_recipe(db_session, http_client, simple_test_data):
    r, ii, i, t = simple_test_data
    http_client.get(f"/api/recipes/{r.id}").raise_for_status()
    http_client.delete(f"/api/recipes/{r.id}").raise_for_status()
    assert not db_session.query(Recipe).filter_by(id=r.id).first()


@pytest.mark.parametrize("image", ["thumbnail_image", "detail_image"])
@pytest.mark.asyncio
async def test_upload_image(db_session, http_client, simple_test_data, dummy_image, image):
    r, _, _, _ = simple_test_data

    path = f"/api/recipes/{r.id}/{image.replace('_', '-')}"
    response = http_client.post(
        path,
        files={
            "image": ("filename", open(dummy_image, "rb"), "image/jpeg")
        }
    )
    response.raise_for_status()
    assert response.status_code == 200

    data = response.json()
    updated_response = RecipeSchema(**data)

    db_session.expunge_all()
    updated_db = db_session.query(Recipe).filter_by(id=r.id).first()

    for updated, index in zip([updated_db, updated_response], ["DB", "RESPONSE"]):
        item = getattr(updated, image)
        assert item, f"EMPTY! - {index}"
        assert item.endswith(".avif"), f"Wrong ext! - {index}"
