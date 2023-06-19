import os
import random

import pytest
from sqlalchemy import create_engine
from sqlmodel import Session

from chef.main import app
from chef.settings import settings
from chef.models import Base, Tag, Ingredient, IngredientItem, Recipe, Category, Unit

from fastapi.testclient import TestClient
import string
import random


@pytest.fixture(scope="session", autouse=True)
def monkeypatch_engine():
    random_db_name = "".join([random.choice(string.ascii_lowercase) for _ in range(10)])
    settings.database_uri = f'sqlite:////tmp/chef-{random_db_name}.db'


@pytest.fixture(scope="function")
def inmemory_engine():
    return create_engine(settings.database_uri)


@pytest.fixture(scope="function")
def http_client() -> TestClient:
    yield TestClient(app)


@pytest.fixture(scope="function")
def db(inmemory_engine):
    Base.metadata.create_all(inmemory_engine)
    yield
    Base.metadata.drop_all(inmemory_engine)


@pytest.fixture(scope="function")
def db_session(db, inmemory_engine) -> Session:
    with Session(inmemory_engine) as session:
        yield session


@pytest.fixture()
def tag():
    def _inner(session: Session, **kwargs):
        t = Tag(**kwargs)
        session.add(t)
        session.commit()
        session.refresh(t)
        return t
    yield _inner


@pytest.fixture()
def ingredient():
    def _inner(session, **kwargs):
        i = Ingredient(**kwargs)
        session.add(i)
        session.commit()
        session.refresh(i)
        return i
    yield _inner


@pytest.fixture()
def ingredient_item():
    def _inner(session: Session, **kwargs):
        i = IngredientItem(**kwargs)
        session.add(i)
        session.commit()
        session.refresh(i)
        return i
    yield _inner


@pytest.fixture()
def recipe():
    def _inner(session: Session, **kwargs):
        r = Recipe(**kwargs)
        session.add(r)
        session.commit()
        session.refresh(r)
        return r
    yield _inner


@pytest.fixture()
def category():
    def _inner(session, **kwargs):
        c = Category(**kwargs)
        session.add(c)
        session.commit()
        session.refresh(c)
        return c

    yield _inner


@pytest.fixture()
def simple_test_data(db_session, tag, ingredient, ingredient_item, recipe):
    i = ingredient(db_session, name="ingredient")
    ii = IngredientItem(ingredient=i, unit=Unit(name="kg", grams=1000.0))
    t = tag(db_session, name="tag")
    r = recipe(db_session, title="recipe_01", ingredients=[ii])
    return r, ii, i, t


@pytest.fixture()
def category_with_tag(db_session, category, tag):
    t = tag(db_session, name="tag")
    c = category(db_session, name="italian food", tags=[t])
    return c, t


@pytest.fixture()
def dummy_image():
    path = os.path.join(os.path.dirname(__file__), "data", "test_image.jpg")
    assert os.path.isfile(path)
    return path
