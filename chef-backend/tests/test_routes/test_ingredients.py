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
