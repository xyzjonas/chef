from app.models import Category


def test_category_dict(tag):
    t = tag(name="tag-01")
    data = {
        "name": "best food ever"
    }
    c = Category(name=data["name"], tags=[t])
    assert c.dictionary
    assert c.dictionary["name"] == data["name"]
    assert c.dictionary["tags"] == [t.dictionary]
