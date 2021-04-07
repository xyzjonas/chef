import json
from flask import jsonify, request

from app import db
from app.main import bp
from app.models import Recipe, Tag, Ingredient, IngredientItem


def _assert_request_data(data: dict, required=None):
    required = required or []
    if not data:
        return "No data received.", 400

    for req in required:
        if req not in data:
            return f"'{req}' field is required.", 400


def _validate_type(val, typ3):
    if type(val) is not typ3:
        raise InvalidUsage(
            f"{val} is of type {type(val)} instead of required '{typ3}'", status_code=400)
    return True


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@bp.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@bp.route('/', methods=['GET'])
def root():
    data = {
        "tags": [tag.dictionary for tag in Tag.query.all()]
    }
    return jsonify(data), 200


@bp.route('/recipes', methods=['GET'])
def get_recipes():
    i = "draft" in request.args
    drafts = request.args.get("draft", default=False, type=json.loads)
    ingredients = request.args.get("ingredients", default=None)

    recipes = Recipe.query.filter_by(draft=drafts).all()
    if ingredients:
        for i in ingredients.split(","):
            def has_ingredient(recipe):
                return i in [ing.ingredient.name for ing in recipe.ingredients]
            recipes = filter(has_ingredient, recipes)

    recipes = [recipe.get_dictionary(depth=2, exclude=["body"]) for recipe in recipes]
    return jsonify(recipes), 200


@bp.route('/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    return jsonify([tag.dictionary for tag in tags]), 200


@bp.route('/tags/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first_or_404()
    return jsonify(tag.dictionary), 200


@bp.route('/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    return f"{tag} deleted.", 200


@bp.route('/ingredients', methods=['GET'])
def get_ingredients():
    ingredients = Ingredient.query.all()
    return jsonify([i.dictionary for i in ingredients]), 200


@bp.route('/ingredients/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id):
    ingredient = Ingredient.query.filter_by(id=ingredient_id).first_or_404()
    return jsonify(ingredient), 200


@bp.route('/tags/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id):
    ingredient = Ingredient.query.filter_by(id=ingredient_id).first_or_404()
    db.session.delete(ingredient)
    db.session.commit()
    return f"{ingredient} deleted.", 200


@bp.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    return jsonify(recipe.dictionary), 200


@bp.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    recipe_repr = str(recipe)
    db.session.delete(recipe)
    db.session.commit()
    return f"{recipe_repr} deleted.", 200


@bp.route('/recipes/<int:recipe_id>/text', methods=['GET'])
def recipes_get_body(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    return str(recipe.body), 200


# todo: rename to 'post'
@bp.route('/recipes/new', methods=['POST'])
def new_recipe():
    data = request.json or request.form

    created = False

    if data.get("id"):
        recipe = Recipe.query.filter_by(id=data.get("id")).first_or_404()
    else:
        _assert_request_data(data, required=["title"])
        _validate_type(data["title"], str)
        recipe = Recipe(title=data["title"])
        created = True

    if data.get("title") and _validate_type(data.get("title"), str):
        recipe.title = data["title"]
    if data.get("subtitle") and _validate_type(data.get("subtitle"), str):
        recipe.subtitle = data["subtitle"]
    if data.get("source_name") and _validate_type(data.get("source_name"), str):
        print("!!! SOURCE NAME: {}".format(data["source_name"]))
        recipe.source_name = data["source_name"]
    if data.get("source") and _validate_type(data.get("source"), str):
        recipe.source = data["source"]
    if data.get("body") and _validate_type(data.get("body"), str):
        recipe.body = data["body"]
    if data.get("draft") and _validate_type(data.get("draft"), bool):
        recipe.draft = data["draft"]

    # ingredients
    ingredient_items = []
    for item in (data.get("ingredients") or []):
        if not item.get("ingredient") or not item["ingredient"].get("name"):
            raise InvalidUsage(f"Malformed: one of the posted ingredients is missing 'name' field",
                               status_code=404)
        ingredient_name = item["ingredient"].get("name")
        ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
        if not ingredient:
            ingredient = Ingredient(name=ingredient_name)

        ii = IngredientItem(ingredient=ingredient, amount=item.get("amount"), unit=item.get("unit"))
        ingredient_items.append(ii)
    recipe.ingredients = ingredient_items

    # tags
    tags = set()
    for t in (data.get("tags") or []):
        tag = Tag.query.filter_by(name=t.get("name")).first()
        if not tag and t.get("name"):
            tag = Tag(name=t.get("name"))
        tags.add(tag)
    recipe.tags = list(tags)

    db.session.add(recipe)
    db.session.commit()
    if created:
        return f"{recipe.title} created.", 201
    else:
        return f"{recipe.title} modified.", 200


@bp.route('/recipes/<int:recipe_id>', methods=['POST'])
def modify_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    data = request.json or request.form
    _assert_request_data(data, required=["title"])

    recipe.title = data["title"]
    recipe.body = data["body"]
    db.session.add(recipe)
    db.session.commit()
    return f"{recipe.title} modified", 200
