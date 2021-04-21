import pytest

from app.models import Recipe, Ingredient, IngredientItem, Tag, Unit


def test_get_recipes(test_app, simple_test_data):
    recipe, ii, i, t = simple_test_data

    with test_app.test_client() as client:
        response = client.get("/recipes")
        assert response.status_code == 200
        assert response.is_json
        assert type(response.json) is list
        assert len(response.json) == 1
        assert response.json[0] == recipe.get_dictionary(depth=2, exclude=["body"])


def test_get_recipes_filter(test_app, simple_test_data):
    with test_app.test_client() as client:
        response = client.get("/recipes?draft=true")
        assert response.status_code == 200
        assert response.is_json
        assert type(response.json) is list
        assert len(response.json) == 0


def test_get_recipe_filter_ingredient(test_app, simple_test_data):
    r, ii, i, t = simple_test_data

    with test_app.test_client() as client:
        response = client.get(f"/recipes?ingredients={i.name}")
        assert response.status_code == 200
        assert response.is_json
        assert type(response.json) is list
        assert len(response.json) == 1


def test_get_recipe_filter_ingredient_negative(test_app, simple_test_data):
    with test_app.test_client() as client:
        response = client.get(f"/recipes?ingredients=madeup")
        assert response.status_code == 200
        assert response.is_json
        assert type(response.json) is list
        assert len(response.json) == 0


def test_add_recipe_minimal(test_app):
    with test_app.test_client() as client:
        response = client.post("/recipes/new", json={"title": "spaghetti"})
        assert response.status_code == 201
    assert Recipe.query.filter_by(title="spaghetti").first()


@pytest.mark.parametrize("data", [
    {"title": 123},
    {"title": "test", "subtitle": 123},
    {"title": "test", "source": 123},
    {"title": "test", "source_name": 123},
    {"title": "test", "draft": "true"},
    {"title": "test", "body": 123},
], ids=["title", "subtitle", "source", "source_name", "draft", "body"])
def test_add_recipe_invalid_type(test_app, data):
    with test_app.test_client() as client:
        response = client.post("/recipes/new", json=data)
        assert response.status_code == 400


def test_add_recipe(test_app):
    data = {
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
        "draft": True
    }

    with test_app.test_client() as client:
        response = client.post("/recipes/new", json=data)
        assert response.status_code == 201

    r = Recipe.query.filter_by(title="Test").first()
    assert r
    assert r.title == "Test"
    assert r.subtitle == "subtitle"
    assert r.source == "source"
    assert r.source_name == "source_name"
    assert r.body == "body"
    assert r.draft
    assert r.portions == 20

    assert Tag.query.filter_by(name="tag").first()
    assert Ingredient.query.filter_by(name="rice").first()
    assert Unit.query.filter_by(name="g").first()


@pytest.mark.parametrize("fist_unit", [None, {"name": "g"}], ids=["none", "g"])
def test_add_recipe_no_unit(test_app, fist_unit):
    data = {
        "ingredients": [
            {"amount": "100", "ingredient": {"name": "rice"}}
        ],
        "title": "Test",
    }
    if fist_unit:
        data["ingredients"][0]["unit"] = fist_unit

    with test_app.test_client() as client:
        response = client.post("/recipes/new", json=data)
        assert response.status_code == 201

    r = Recipe.query.filter_by(title=data["title"]).first()
    assert r
    assert r.title == data["title"]
    assert len(r.ingredients) == 1
    assert r.ingredients[0].ingredient.name == data["ingredients"][0]["ingredient"]["name"]
    assert r.ingredients[0].unit.name == data["ingredients"][0]["unit"]["name"] \
        if fist_unit else "pcs"

    data["id"] = r.id
    data["ingredients"][0]["unit"] = {}
    with test_app.test_client() as client:
        response = client.post("/recipes/new", json=data)
        assert response.status_code == 200

    r = Recipe.query.filter_by(title="Test").first()
    assert r
    assert r.title == "Test"
    assert len(r.ingredients) == 1
    assert r.ingredients[0].ingredient.name == "rice"
    assert r.ingredients[0].unit.name == "pcs"


def test_edit_recipe(test_app, simple_test_data):
    r, ii, i, t = simple_test_data
    data = {
        "id": r.id,
        "ingredients": [
            {"amount": "100", "unit": {"name": "g"}, "ingredient": {"name": "rice"}}
        ],
        "tags": [
            {"name": "tag"}
        ],
        "title": "TestThisShouldBeRandom",
        "subtitle": "subtitle that never occurred before",
        "portions": 20,
        "source": "source",
        "source_name": "source_name",
        "body": "body",
        "draft": True,
    }

    with test_app.test_client() as client:
        response = client.post("/recipes/new", json=data)
        assert response.status_code == 200

    r = Recipe.query.filter_by(title="TestThisShouldBeRandom").first()
    assert r
    assert r.title == "TestThisShouldBeRandom"
    assert r.subtitle == "subtitle that never occurred before"
    assert r.source == "source"
    assert r.source_name == "source_name"
    assert r.body == "body"
    assert r.portions == 20
    assert r.draft

    assert Tag.query.filter_by(name="tag").first()
    assert Ingredient.query.filter_by(name="rice").first()
    assert Unit.query.filter_by(name="g").first()


def test_delete_recipe(test_app, simple_test_data):
    r, ii, i, t = simple_test_data
    with test_app.test_client() as client:
        response = client.delete(f"/recipes/{r.id}")
        assert response.status_code == 200
    assert not Recipe.query.filter_by(id=r.id).first()