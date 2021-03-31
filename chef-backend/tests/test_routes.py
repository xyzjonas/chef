from app import db
from app.models import Recipe, Ingredient, IngredientItem, Tag


def test_get_recipes(test_app, simple_test_data):
    recipe, ii, i = simple_test_data

    with test_app.test_client() as client:
        response = client.get("/recipes")
        assert response.status_code == 200
        assert response.is_json
        assert type(response.json) is list
        assert len(response.json) == 1
        assert response.json[0] == recipe.dictionary


def test_add_recipe_minimal(test_app):
    with test_app.test_client() as client:
        response = client.post("/recipes/new", json={"title": "spaghetti"})
        assert response.status_code == 201
    assert Recipe.query.filter_by(title="spaghetti").first()


def test_add_recipe(test_app):
    data = {
        "ingredients": [
            {"amount": "100", "unit": "g", "name": "rice"}
        ],
        "tags": [
            {"name": "tag"}
        ],
        "title": "Test"}
    with test_app.test_client() as client:
        response = client.post("/recipes/new", json=data)
        assert response.status_code == 201

    assert Recipe.query.filter_by(title="Test").first()
    assert Tag.query.filter_by(name="tag").first()
    assert Ingredient.query.filter_by(name="rice").first()


def test_delete_recipe(test_app, simple_test_data):
    r, ii, i = simple_test_data
    with test_app.test_client() as client:
        response = client.delete(f"/recipes/{r.id}")
        assert response.status_code == 200
    assert not Recipe.query.filter_by(id=r.id).first()


def test_get_tags():
    assert False


def test_get_tag():
    assert False


def test_delete_tag():
    assert False

