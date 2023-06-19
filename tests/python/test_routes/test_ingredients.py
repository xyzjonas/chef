import pytest
from sqlalchemy.orm import Session

from chef.models import Recipe, Ingredient
from chef.schemas import Ingredient as I


def _assert_ingredient_matches(session: Session, ingredient: dict):
    db_item = session.query(Ingredient).filter_by(name=ingredient["name"]).first()
    assert I(**db_item.dictionary) == I(**ingredient)


@pytest.mark.parametrize("size", [1, 10])
def test_get_ingredients(http_client, db_session, ingredient, size):
    ingredients = [ingredient(db_session, name=f"ingredient-{i}") for i in range(size)]
    response = http_client.get(f"/api/ingredients")
    assert response.status_code == 200
    assert type(response.json()) is list
    assert len(response.json()) == size == len(ingredients)

    expected_ingredients = [I(**ing.dictionary) for ing in ingredients]
    assert response.json() == [ing.dict() for ing in expected_ingredients]


def test_get_ingredient(http_client, db_session, ingredient):
    ingredient = ingredient(db_session, name="leak", energy=11.1)
    response = http_client.get(f"/api/ingredients/{ingredient.id}")
    assert response.status_code == 200
    assert response.json() == I(**ingredient.dictionary)


def test_delete_ingredient(http_client, db_session, ingredient):
    ingredient = ingredient(db_session, name="carrot", energy=11.1)
    response = http_client.delete(f"/api/ingredients/{ingredient.id}")
    assert response.status_code == 200
    assert not db_session.query(Ingredient).filter_by(id=ingredient.id).first()


def test_delete_with_existing_item(db_session, http_client, simple_test_data):
    r, ii, i, t = simple_test_data
    response = http_client.delete(f"/api/ingredients/{i.id}")
    assert response.status_code == 400
    assert db_session.query(Ingredient).filter_by(id=i.id).first()


def test_delete_with_deleted_recipe(db_session, http_client, simple_test_data):
    r, ii, i, t = simple_test_data
    response = http_client.delete(f"/api/recipes/{r.id}")
    assert response.status_code == 200
    assert not db_session.query(Recipe).filter_by(id=r.id).first()

    response = http_client.delete(f"/api/ingredients/{i.id}")
    assert response.status_code == 200
    assert not db_session.query(Ingredient).filter_by(id=i.id).first()


def test_update(db_session, http_client, simple_test_data):
    r, ii, i, t = simple_test_data

    response = http_client.get(f"/api/ingredients/{i.id}")
    response.raise_for_status()
    _assert_ingredient_matches(db_session, response.json())

    data = {
        "name": "new and better name",
        "energy": 111.1,
        "carbs": 222.2,
        "fats": 333.3,
        "proteins": 444.4,
        "fibres": 5,
        "salt": 60,
    }

    response = http_client.put(f"/api/ingredients/{i.id}", json=data)
    assert response.status_code == 200

    db_session.expire_all()
    i = db_session.query(Ingredient).filter_by(name="new and better name").first()
    assert i
    assert i.energy == data["energy"]
    assert i.carbs == data["carbs"]
    assert i.fats == data["fats"]
    assert i.proteins == data["proteins"]
    assert i.fibres == data["fibres"]
    assert i.salt == data["salt"]


@pytest.mark.parametrize("data", [
    {"name": "new and better name", "energy": "asd"},
    {"name": "new and better name", "carbs": "asd"},
    {"name": "new and better name", "fats": "asd"},
    {"name": "new and better name", "proteins": "asd"},
    {"name": "new and better name", "fibres": "asd"},
    {"name": "new and better name", "salt": "asd"},
])
def test_create_ingredient_invalid_data_type(http_client, simple_test_data, data):
    r, ii, i, t = simple_test_data
    data["id"] = i.id
    response = http_client.put(f"/api/ingredients/{i.id}", json=data)
    assert response.status_code == 422
