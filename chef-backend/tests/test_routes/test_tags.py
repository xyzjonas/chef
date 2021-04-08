import pytest

from app.models import Recipe, Ingredient, IngredientItem, Tag


@pytest.mark.parametrize("size", [10])
def test_get_tags(test_app, tag, size):
    tags = [tag(name=f"tag-{i}") for i in range(size)]
    with test_app.test_client() as client:
        response = client.get(f"/tags")
        assert response.status_code == 200
        assert response.is_json
        assert type(response.json) is list
        assert len(response.json) == size == len(tags)
        for t in tags:
            assert t.dictionary in response.json


def test_get_tag(test_app, tag):
    tag = tag(name="tag-1")
    with test_app.test_client() as client:
        response = client.get(f"/tags/{tag.id}")
        assert response.status_code == 200
        assert response.is_json
        assert response.json == tag.dictionary


def test_delete_tag(test_app, tag):
    tag = tag(name="china")
    with test_app.test_client() as client:
        response = client.delete(f"/tags/{tag.id}")
        assert response.status_code == 200
    assert not Ingredient.query.filter_by(id=tag.id).first()


