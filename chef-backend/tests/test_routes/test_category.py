from app.models import Category, Tag


def test_add_category(test_app):
    data = {
        "tags": [
            {"name": "tag"}
        ],
        "name": "the best food ever",
    }

    with test_app.test_client() as client:
        response = client.post("/categories", json=data)
        assert response.status_code == 201

    c = Category.query.filter_by(name=data["name"]).first()
    assert c
    assert c.name == data["name"]

    tag = Tag.query.filter_by(name="tag").first()
    assert tag
    assert c.tags
    assert c.tags[0] == tag


def test_modify_category(test_app, category_with_tag):
    c, t = category_with_tag

    data = {
        "id": c.id,
        "name": c.name + "-modified",
        "tags": [
            {"name": t.name + "-1"},
            {"name": t.name + "-2"},
        ],
    }

    with test_app.test_client() as client:
        response = client.post("/categories", json=data)
        assert response.status_code == 200

    c = Category.query.filter_by(id=data["id"]).first()
    assert c
    assert c.name == data["name"]
    assert len(c.tags) == 2


def test_get_categories(test_app, category_with_tag):
    c, t = category_with_tag

    with test_app.test_client() as client:
        response = client.get("/categories")
        assert response.status_code == 200
        assert response.is_json
        assert type(response.json) is list
        categories = response.json
    assert len(categories) == 1
    assert categories[0] == c.dictionary


def test_delete_category(test_app, category_with_tag):
    c, t = category_with_tag
    with test_app.test_client() as client:
        response = client.delete(f"/categories/{c.id}")
        assert response.status_code == 200
    assert len(Category.query.all()) == 0
