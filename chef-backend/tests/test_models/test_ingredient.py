import pytest

from app import db
from app.models import Recipe, IngredientItem, Ingredient, Tag, Base


def test_ingredient_dict_default(ingredient):
    ingredient = ingredient(name="onion")
    assert ingredient.salt == 0.0
    assert ingredient.fats == 0.0
    assert ingredient.carbs == 0.0
    assert ingredient.energy == 0.0
    assert ingredient.protein == 0.0
    assert ingredient.density == 1000
    assert not ingredient.is_liquid


def test_ingredient_dict(ingredient):
    test_items = {
        "id": None,
        "salt": 125.99,
        "fats": 124.99,
        "carbs": 123.99,
        "energy": 122.99,
        "protein": 121.99,
        "density": 120.99,
        "is_liquid": True,
        "name": "sweet potato",
    }

    i = ingredient(
        name=test_items["name"],
        salt=test_items["salt"],
        fats=test_items["fats"],
        carbs=test_items["carbs"],
        energy=test_items["energy"],
        protein=test_items["protein"],
        density=test_items["density"],
        is_liquid=test_items["is_liquid"],
    )
    assert i.dictionary
    assert len(i.dictionary) == len(Ingredient.__items__) == len(test_items)
    assert i.dictionary.get("id")
    assert i.dictionary["name"] == test_items["name"]
    assert i.dictionary["salt"] == test_items["salt"]
    assert i.dictionary["fats"] == test_items["fats"]
    assert i.dictionary["carbs"] == test_items["carbs"]
    assert i.dictionary["energy"] == test_items["energy"]
    assert i.dictionary["protein"] == test_items["protein"]
    assert i.dictionary["density"] == test_items["density"]
    assert i.dictionary["is_liquid"] == test_items["is_liquid"]


def test_ingredient_item_dict(ingredient, ingredient_item):
    name = "ingredient"
    i = ingredient(name=name)

    amount = 10
    unit = "kg"
    note = "note"
    ii = IngredientItem(ingredient=i, amount=amount, unit=unit, note=note)

    assert ii.dictionary
    assert len(ii.dictionary) == 4
    # no id in ingredient item
    assert ii.dictionary["amount"] == amount
    assert ii.dictionary["unit"] == unit
    assert ii.dictionary["note"] == note
    assert ii.dictionary["ingredient"] == i.dictionary
