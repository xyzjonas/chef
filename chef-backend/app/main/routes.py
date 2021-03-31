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


@bp.route('/', methods=['GET'])
def root():
    data = {
        "tags": [tag.dictionary for tag in Tag.query.all()]
    }
    return jsonify(data), 200


@bp.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = [recipe.get_dictionary(depth=2, exclude=["body"]) for recipe in Recipe.query.all()]
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


@bp.route('/recipes/new', methods=['POST'])
def new_recipe():
    data = request.json or request.form
    _assert_request_data(data, required=["title"])
    recipe = Recipe(
        title=data["title"],
        subtitle=data.get("subtitle"),
        source_name=data.get("source_name"),
        source=data.get("source"),
        ingredients=[],
        tags=[],
        body=data.get("body")
    )

    # ingredients
    ingredient_items = []
    for i in (data.get("ingredients") or []):
        ingredient = Ingredient.query.filter_by(name=i.get("name")).first()
        if not ingredient and i.get("name"):
            ingredient = Ingredient(name=i.get("name"))
        ii = IngredientItem(ingredient=ingredient, amount=i.get("amount"), unit=i.get("unit"))
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
    return f"{recipe.title} created.", 201


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
