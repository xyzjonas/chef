import pytest

from app import db
from app.models import Recipe, IngredientItem, Ingredient


def test_ingredient_dict(ingredient):
    name = "ingredient"
    i = ingredient(name=name)
    assert i.dictionary
    assert len(i.dictionary) == 2
    assert i.dictionary.get("id")
    assert i.dictionary["name"] == name


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


def test_recipe_dictionary(recipe, ingredient, ingredient_item):
    i = ingredient(name="ingredient")
    ii = IngredientItem(ingredient=i)

    title = "recipe_01"
    subtitle = "recipe_01"
    body = "asd"
    source = "http://source.com"
    recipe = recipe(title=title, subtitle=subtitle, ingredients=[ii], body=body, source=source)
    assert recipe
    assert recipe.dictionary
    assert len(recipe.dictionary) == 6
    assert recipe.dictionary.get("id")
    assert recipe.dictionary["title"] == title
    assert recipe.dictionary["subtitle"] == subtitle
    assert recipe.dictionary["source"] == source
    assert recipe.dictionary["concat"] == body + "..."
    assert len(recipe.dictionary["ingredients"]) == len(recipe.ingredients) == 1
    assert recipe.dictionary["ingredients"][0] == ii.dictionary
