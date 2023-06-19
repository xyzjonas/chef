from chef.models import Category


def test_category_dict(tag, db_session):
    t = tag(db_session, name="tag-01")
    data = {
        "name": "best food ever"
    }
    c = Category(name=data["name"], tags=[t])
    assert c.dictionary
    assert c.dictionary["name"] == data["name"]
    assert c.dictionary["tags"] == [t.dictionary]
