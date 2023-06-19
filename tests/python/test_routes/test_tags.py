import pytest

from chef.models import Ingredient, Tag


@pytest.mark.parametrize("size", [10])
def test_get_tags(http_client, db_session, tag, size):
    tags = [
        tag(db_session, name=f"tag-{i}") for i in range(size)
    ]
    response = http_client.get("/api/tags")
    assert response.status_code == 200
    data = response.json()
    assert type(data) is list
    assert len(data) == size == len(tags)
    for t in tags:
        assert t.dictionary in response.json()


@pytest.mark.parametrize("name", ["tag-1"])
def test_get_tag(db_session, http_client, tag, name):
    tag = tag(db_session, name=name)
    response = http_client.get(f"/api/tags/{tag.id}")
    assert response.status_code == 200
    assert response.json() == tag.dictionary


def test_create_tag(db_session, http_client):
    tag_name = "foobar"
    response = http_client.post("/api/tags", json={"name": tag_name})
    response.raise_for_status()
    assert response.status_code == 201
    tag = response.json()

    t = db_session.query(Tag).filter_by(name=tag_name).first()
    assert t.id == tag["id"]


def test_delete_tag(db_session, http_client, tag):
    tag = tag(db_session, name="chinese")
    http_client.delete(f"/api/tags/{tag.id}").raise_for_status()
    assert not db_session.query(Ingredient).filter_by(id=tag.id).first()


