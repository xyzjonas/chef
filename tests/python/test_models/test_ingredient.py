from chef.models import IngredientItem, Ingredient, Unit


def test_ingredient_dict_default(db_session, ingredient):
    ingredient = ingredient(db_session, name="onion")
    assert ingredient.name == "onion"
    assert ingredient.approx_per_piece == 0.0

    assert ingredient.energy == 0.0
    assert ingredient.fats == 0.0
    assert ingredient.carbs == 0.0
    assert ingredient.proteins == 0.0
    assert ingredient.fibres == 0.0
    assert ingredient.salt == 0.0

    assert ingredient.density == 1000
    assert not ingredient.is_liquid


def test_ingredient_dict(db_session, ingredient):
    data = {
        "id": None,
        "salt": 125.99,
        "fats": 124.99,
        "carbs": 123.99,
        "energy": 122.99,
        "proteins": 121.99,
        "fibres": 129.99,
        "density": 120.99,
        "is_liquid": True,
        "name": "sweet potato",
    }

    i = ingredient(
        db_session,
        name=data["name"],
        salt=data["salt"],
        fats=data["fats"],
        carbs=data["carbs"],
        fibres=data["fibres"],
        energy=data["energy"],
        proteins=data["proteins"],
        density=data["density"],
        is_liquid=data["is_liquid"],
    )
    assert i.dictionary
    x = i.dictionary
    assert len(i.dictionary) == len(Ingredient.__items__) == len(data)
    assert i.dictionary.get("id")
    assert i.dictionary["name"] == data["name"]
    assert i.dictionary["salt"] == data["salt"]
    assert i.dictionary["fats"] == data["fats"]
    assert i.dictionary["carbs"] == data["carbs"]
    assert i.dictionary["energy"] == data["energy"]
    assert i.dictionary["proteins"] == data["proteins"]
    assert i.dictionary["density"] == data["density"]
    assert i.dictionary["is_liquid"] == data["is_liquid"]


def test_ingredient_item_dict(db_session, ingredient, ingredient_item):
    name = "ingredient"
    i = ingredient(db_session, name=name)

    amount = 10.0
    unit = Unit(name="kg")
    note = "note"
    ii = IngredientItem(ingredient=i, amount=amount, unit=unit, note=note)

    db_session.add(ii)
    db_session.commit()
    assert ii.id

    assert ii.dictionary
    assert len(ii.dictionary) == 5
    assert ii.dictionary["id"] == ii.id
    assert ii.dictionary["amount"] == amount
    assert ii.dictionary["unit"] == {'id': 1, 'name': 'kg', 'grams': 0.0}
    assert ii.dictionary["note"] == note
    assert ii.dictionary["ingredient"] == i.dictionary


def test_ingredient_empty(db_session, ingredient):
    name = "ingredient"
    i = ingredient(db_session, name=name)

    ii = IngredientItem(ingredient=i)
    db_session.add(ii)
    db_session.commit()
    assert ii.id
    assert ii.dictionary
    assert len(ii.dictionary) == 5
    assert ii.dictionary["id"] == ii.id
    assert ii.dictionary["amount"] is None
    assert ii.dictionary["unit"] is None
    assert ii.dictionary["note"] is None
    assert ii.dictionary["ingredient"] == i.dictionary

