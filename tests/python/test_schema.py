from chef.models import Recipe as RecipeDb
from chef.schemas import Recipe


def test_foo():
    item = RecipeDb(title="foo bar")
    x = 1