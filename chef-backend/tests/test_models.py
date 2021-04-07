import pytest

from app import db
from app.models import Recipe, IngredientItem, Ingredient, Tag, Base


def test_ingredient_dict(ingredient):
    name = "ingredient"
    i = ingredient(name=name)
    assert i.dictionary
    assert len(i.dictionary) == 2
    assert i.dictionary.get("id")
    assert i.dictionary["name"] == name


def test_ingredient_item_dict(ingredient, ingredient_item):
    name = "ingredient"
    i = ingredient(name=name)

    amount = 10
    unit = "kg"
    note = "note"
    ii = IngredientItem(ingredient=i, amount=amount, unit=unit, note=note)

    assert ii.dictionary
    assert len(ii.dictionary) == 4
    # no id in ingredient item
    assert ii.dictionary["amount"] == amount
    assert ii.dictionary["unit"] == unit
    assert ii.dictionary["note"] == note
    assert ii.dictionary["ingredient"] == i.dictionary

    """
    <template>
  <div id="app">    
    <Navbar/>

    <div>
      <HelloWorld msg="This is the way!"/>
    </div>

    <router-view></router-view>
    <hr>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import Navbar from './components/common/Navbar.vue'

export default {
  name: 'App',
  components: {
    HelloWorld,
    Navbar
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

    """


def test_recipe_dictionary(recipe, ingredient, ingredient_item):
    i = ingredient(name="ingredient")
    ii = IngredientItem(ingredient=i)
    t = Tag(name="tag")

    test_items = {
        "id": None,
        "title": "recipe_01",
        "subtitle": "recipe_01",
        "body": "asd",
        "source": "http://source.com",
        "source_name": "source",
        "ingredients": [ii],
        "tags": [t],
    }
    assert len(test_items) == len(Recipe.__items__)

    recipe = recipe(
        title=test_items["title"],
        subtitle=test_items["subtitle"],
        body=test_items["body"],
        source=test_items["source"],
        source_name=test_items["source_name"],
        ingredients=test_items["ingredients"],
        tags=test_items["tags"],
    )
    db.session.add(recipe)
    db.session.commit()
    test_items['id'] = recipe.id

    assert recipe
    assert recipe.dictionary
    assert recipe.dictionary["id"] == test_items["id"]
    assert recipe.dictionary["title"] == test_items["title"]
    assert recipe.dictionary["subtitle"] == test_items["subtitle"]
    assert recipe.dictionary["body"] == test_items["body"]
    assert recipe.dictionary["source"] == test_items["source"]
    assert recipe.dictionary["source_name"] == test_items["source_name"]

    assert len(recipe.dictionary["ingredients"]) == len(recipe.ingredients) == 1
    assert recipe.dictionary["ingredients"][0] == ii.dictionary

    assert len(recipe.dictionary["tags"]) == len(recipe.tags) == 1
    assert recipe.dictionary["tags"][0] == t.dictionary


def test_dictionary_exclude(simple_test_data):
    r, ii, i = simple_test_data
    assert "title" in r.get_dictionary()
    assert "title" not in r.get_dictionary(exclude=["title"])


def test_tag(recipe):
    r = recipe(title="chicken")
    tag = Tag(name="edible")
    r.tags.append(tag)
    assert r.dictionary["tags"][0]["name"] == "edible"
