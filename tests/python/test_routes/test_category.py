import pytest

from chef.models import Category, Tag


def test_get_categories(http_client, category_with_tag):
    c, t = category_with_tag

    response = http_client.get("/api/categories")
    assert response.status_code == 200
    assert type(response.json()) is list
    categories = response.json()
    assert len(categories) == 1
    assert categories[0] == c.dictionary


def test_create_category(db_session, tag, http_client):
    tag_name = "foo bar"
    t = tag(db_session, name=tag_name)
    data = {
        "tags": [{"id": t.id}],
        "name": "the best food category ever!",
    }

    response = http_client.post("/api/categories", json=data)
    assert response.status_code == 201

    c = db_session.query(Category).filter_by(name=data["name"]).first()
    assert c
    assert c.name == data["name"]

    tag = db_session.query(Tag).filter_by(name=tag_name).first()
    assert tag
    assert c.tags
    assert c.tags[0] == tag


def test_update_category(http_client, db_session, category, tag):
    cat = category(db_session, name="foobar")
    tag = tag(db_session, name="baz")

    response = http_client.get(f"/api/categories/{cat.id}")
    response.raise_for_status()
    data = response.json()
    assert data["name"] == "foobar"
    assert not data["tags"]

    data = cat.dictionary
    data["tags"] = [{"id": tag.id}]

    response = http_client.put(f"/api/categories/{cat.id}", json=data)
    response.raise_for_status()
    assert response.status_code == 200

    tag_data = tag.dictionary
    db_session.expire_all()

    all_categories = db_session.query(Category).all()
    assert len(all_categories) == 1, 'more than 1 category!'
    c = [c for c in all_categories if c.id == data["id"]]
    assert len(all_categories) == 1, 'the wrong category!'
    c = c[0]
    assert c
    assert c.name == data["name"]
    assert len(c.tags) == 1
    assert c.tags[0].dictionary == tag_data


def test_delete_category(db_session, http_client, category_with_tag):
    c, t = category_with_tag

    response = http_client.delete(f"/api/categories/{c.id}")
    assert response.status_code == 200
    assert len(db_session.query(Category).all()) == 0
