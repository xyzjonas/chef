import pytest

from app.models import Recipe, Ingredient, IngredientItem, Tag


@pytest.mark.parametrize("size", [10])
def test_get_ingredients(test_app, ingredient, size):
    ingredients = [ingredient(name=f"ingredient-{i}") for i in range(size)]
    with test_app.test_client() as client:
        response = client.get(f"/ingredients")
        assert response.status_code == 200
        assert response.is_json
        assert type(response.json) is list
        assert len(response.json) == size == len(ingredients)
        for i in ingredients:
            assert i.dictionary in response.json


def test_get_ingredient(test_app, ingredient):
    ingredient = ingredient(name="leak", energy=11.1)
    with test_app.test_client() as client:
        response = client.get(f"/ingredients/{ingredient.id}")
        assert response.status_code == 200
        assert response.is_json
        assert response.json == ingredient.dictionary


def test_delete_ingredient(test_app, ingredient):
    ingredient = ingredient(name="carrot", energy=11.1)
    with test_app.test_client() as client:
        response = client.delete(f"/ingredients/{ingredient.id}")
        assert response.status_code == 200
    assert not Ingredient.query.filter_by(id=ingredient.id).first()


def test_delete_with_existing_item(test_app, simple_test_data):
    r, ii, i, t = simple_test_data
    with test_app.test_client() as client:
        response = client.delete(f"/ingredients/{i.id}")
        assert response.status_code == 400
    assert Ingredient.query.filter_by(id=i.id).first()


def test_delete_with_deleted_recipe(test_app, simple_test_data):
    r, ii, i, t = simple_test_data
    with test_app.test_client() as client:
        response = client.delete(f"/recipes/{r.id}")
        assert response.status_code == 200
    assert not Recipe.query.filter_by(id=r.id).first()

    with test_app.test_client() as client:
        response = client.delete(f"/ingredients/{i.id}")
        assert response.status_code == 200
    assert not Ingredient.query.filter_by(id=i.id).first()


def test_modify(test_app, simple_test_data):
    r, ii, i, t = simple_test_data

    data = {
        "name": "new and better name",
        "energy": 111.1,
        "carbs": 111.1,
        "fats": 111.1,
        "proteins": 111.1,
        "fibres": 111.1,
        "salt": 111.1,
    }

    with test_app.test_client() as client:
        response = client.post(f"/ingredients/{i.id}", json=data)
        assert response.status_code == 200

    i = Ingredient.query.filter_by(name="new and better name").first()
    assert i
    assert i.energy == data["energy"]
    assert i.carbs == data["carbs"]
    assert i.fats == data["fats"]
    assert i.proteins == data["proteins"]
    assert i.fibres == data["fibres"]
    assert i.salt == data["salt"]


@pytest.mark.parametrize("data", [
    {"name": 123},
    {"name": "new and better name", "energy": "asd"},
    {"name": "new and better name", "carbs": "asd"},
    {"name": "new and better name", "fats": "asd"},
    {"name": "new and better name", "proteins": "asd"},
    {"name": "new and better name", "fibres": "asd"},
    {"name": "new and better name", "salt": "asd"},
])
def test_add_ingredient_invalid_data_type(test_app, simple_test_data, data):
    r, ii, i, t = simple_test_data
    data["id"] = i.id
    with test_app.test_client() as client:
        response = client.post(f"/ingredients/{i.id}", json=data)
        assert response.status_code == 400
