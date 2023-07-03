from chef.models import Recipe, IngredientItem, Tag


def test_dictionary(db_session, recipe, ingredient, ingredient_item):
    i = ingredient(db_session, name="ingredient")
    ii = IngredientItem(ingredient=i)
    t = Tag(name="tag")

    test_items = {
        "id": None,
        "title": "recipe_01",
        "subtitle": "recipe_01",
        "body": "asd",
        "portions": 20,
        "favorite": True,
        "source": "http://source.com",
        "source_name": "source",
        "ingredients": [ii],
        "tags": [t],
    }
    assert len(test_items) == len(Recipe.__items__)

    recipe = recipe(
        db_session,
        title=test_items["title"],
        subtitle=test_items["subtitle"],
        body=test_items["body"],
        source=test_items["source"],
        favorite=test_items["favorite"],
        source_name=test_items["source_name"],
        portions=test_items["portions"],
        ingredients=test_items["ingredients"],
        tags=test_items["tags"],
    )
    db_session.add(recipe)
    test_items['id'] = recipe.id

    assert recipe
    assert recipe.dictionary
    assert recipe.dictionary["id"] == test_items["id"]
    assert recipe.dictionary["title"] == test_items["title"]
    assert recipe.dictionary["subtitle"] == test_items["subtitle"]
    assert recipe.dictionary["body"] == test_items["body"]
    assert recipe.dictionary["source"] == test_items["source"]
    assert recipe.dictionary["source_name"] == test_items["source_name"]
    assert recipe.dictionary["portions"] == test_items["portions"]
    assert recipe.dictionary["favorite"] == test_items["favorite"]

    assert len(recipe.dictionary["ingredients"]) == len(recipe.ingredients) == 1
    assert recipe.dictionary["ingredients"][0] == ii.dictionary

    assert len(recipe.dictionary["tags"]) == len(recipe.tags) == 1
    assert recipe.dictionary["tags"][0] == t.dictionary


def test_dictionary_exclude(simple_test_data):
    r, ii, i, t = simple_test_data
    assert "title" in r.get_dictionary()
    assert "title" not in r.get_dictionary(exclude=["title"])


def test_tag(db_session, recipe):
    r = recipe(db_session, title="chicken")
    tag = Tag(name="edible")
    r.tags.append(tag)
    assert r.dictionary["tags"][0]["name"] == "edible"
