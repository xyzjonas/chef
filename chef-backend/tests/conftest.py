import os
import pytest

from app import create_app, db
from app.config import TestConfig
from app.models import Recipe, Ingredient, IngredientItem, Tag, Category


@pytest.fixture(autouse=True)
def test_app():
    application = create_app(TestConfig)
    db.drop_all()
    with application.app_context():
        yield application


@pytest.fixture(autouse=True)
def test_db(test_app):
    db.create_all()
    yield
    db.drop_all()


@pytest.fixture()
def tag():
    def _inner(**kwargs):
        t = Tag(**kwargs)
        db.session.add(t)
        db.session.commit()
        db.session.refresh(t)
        return t
    yield _inner


@pytest.fixture()
def ingredient():
    def _inner(**kwargs):
        i = Ingredient(**kwargs)
        db.session.add(i)
        db.session.commit()
        db.session.refresh(i)
        return i
    yield _inner


@pytest.fixture()
def ingredient_item():
    def _inner(**kwargs):
        i = IngredientItem(**kwargs)
        db.session.add(i)
        db.session.commit()
        db.session.refresh(i)
        return i
    yield _inner


@pytest.fixture()
def recipe():
    def _inner(**kwargs):
        r = Recipe(**kwargs)
        db.session.add(r)
        db.session.commit()
        db.session.refresh(r)
        return r
    yield _inner


@pytest.fixture()
def category():
    def _inner(**kwargs):
        c = Category(**kwargs)
        db.session.add(c)
        db.session.commit()
        db.session.refresh(c)
        return c

    yield _inner


@pytest.fixture()
def simple_test_data(tag, ingredient, ingredient_item, recipe):
    i = ingredient(name="ingredient")
    ii = IngredientItem(ingredient=i)
    t = tag(name="tag")
    r = recipe(title="recipe_01", ingredients=[ii])
    return r, ii, i, t


@pytest.fixture()
def category_with_tag(category, tag):
    t = tag(name="tag")
    c = category(name="italian food", tags=[t])
    return c, t


@pytest.fixture()
def test_image():
    path = os.path.join(os.path.dirname(__file__), "props", "test_image.jpg")
    assert os.path.isfile(path)
    return path
