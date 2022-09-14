import json
from flask import jsonify, request, current_app

from app import db
from app.exceptions import InvalidUsage
from app.main import bp
from app.models import Recipe, Tag, Ingredient, IngredientItem, Unit, Category


def _assert_request_data(data: dict, required=None):
    required = required or []
    if not data:
        return "No data received.", 400

    for req in required:
        if req not in data:
            return f"'{req}' field is required.", 400


def _validate_type(val, typ3):
    """Validate incoming data types."""
    if typ3 == float:
        try:
            typ3(val)
            return True
        except Exception as e:
            raise InvalidUsage(
                f"{val} is of type {type(val)} instead of required '{typ3}'", status_code=400)
    else:
        if type(val) != typ3:
            raise InvalidUsage(
                f"{val} is of type {type(val)} instead of required '{typ3}'", status_code=400)
    return True


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
    drafts = request.args.get("draft", default=False, type=json.loads)
    ingredients = request.args.get("ingredients", default=None)
    category = request.args.get("category", default=None)

    recipes = Recipe.query.filter_by(draft=drafts).all()
    if ingredients:
        for i in ingredients.split(","):
            def has_ingredient(recipe):
                return i in [ing.ingredient.name for ing in recipe.ingredients]
            recipes = filter(has_ingredient, recipes)

    if category:
        category = Category.query.filter_by(id=category).first_or_404()
        tags = {tag.name for tag in category.tags}
        current_app.logger.debug(f"Filtering by tags: {tags}")
        recipes = [
            recipe for recipe in recipes if tags.issubset({tag.name for tag in recipe.tags})
        ]

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
    return jsonify(ingredient.dictionary), 200


@bp.route('/ingredients/<int:ingredient_id>', methods=['POST'])
def post_ingredient(ingredient_id):
    ingredient = Ingredient.query.filter_by(id=ingredient_id).first_or_404()
    data = request.json or request.form

    if data.get("name") and _validate_type(data.get("name"), str):
        ingredient.name = data.get("name")
    if data.get("energy") and _validate_type(data.get("energy"), float):
        ingredient.energy = data.get("energy")
    if data.get("carbs") and _validate_type(data.get("carbs"), float):
        ingredient.carbs = data.get("carbs")
    if data.get("fats") and _validate_type(data.get("fats"), float):
        ingredient.fats = data.get("fats")
    if data.get("proteins") and _validate_type(data.get("proteins"), float):
        ingredient.proteins = data.get("proteins")
    if data.get("fibres") and _validate_type(data.get("fibres"), float):
        ingredient.fibres = data.get("fibres")
    if data.get("salt") and _validate_type(data.get("salt"), float):
        ingredient.salt = data.get("salt")

    db.session.add(ingredient)
    db.session.commit()
    return f"Ingredient '{ingredient.name}' modified", 200


@bp.route('/ingredients/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id):
    ingredient = Ingredient.query.filter_by(id=ingredient_id).first_or_404()
    ingredient_items = IngredientItem.query.filter_by(ingredient=ingredient)
    if ingredient_items.count() > 0:
        return f"Some recipes are still using this ingredient, delete those first", 400
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
        # a bit hackish :(
        for ii in recipe.ingredients:
            db.session.delete(ii)
        db.session.commit()
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
        recipe.source_name = data["source_name"]
    if data.get("source") and _validate_type(data.get("source"), str):
        recipe.source = data["source"]
    if data.get("portions") and _validate_type(data.get("portions"), int):
        recipe.portions = data["portions"]
    if data.get("body") and _validate_type(data.get("body"), str):
        recipe.body = data["body"]
    if data.get("draft") and _validate_type(data.get("draft"), bool):
        recipe.draft = data["draft"]

    # ingredients
    ingredient_items = []
    for item in (data.get("ingredients") or []):
        if not item.get("ingredient") or not item["ingredient"].get("name"):
            raise InvalidUsage(f"Malformed: one of the posted ingredients is missing 'name' field",
                               status_code=400)
        ingredient_name = item["ingredient"].get("name")
        ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
        if not ingredient:
            ingredient = Ingredient(name=ingredient_name)

        # unit (input format is same as output)
        if item.get("unit") and item["unit"].get("name"):
            unit = Unit.query.filter_by(name=item["unit"]["name"]).first()
            if not unit:
                unit = Unit(name=item["unit"]["name"])
                db.session.add(unit)
                db.session.commit()
        else:  # default = piece
            unit = Unit.query.filter_by(name="pcs").first() or Unit(name="pcs")

        ii = IngredientItem(ingredient=ingredient, amount=item.get("amount"),
                            unit=unit, note=item.get("note"))
        ingredient_items.append(ii)
    recipe.ingredients = ingredient_items

    # tags
    tags = set()
    for t in (data.get("tags") or []):
        tag_name = t.get("name")
        if not tag_name:
            continue
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
        tags.add(tag)
    recipe.tags = list(tags)

    db.session.add(recipe)
    db.session.commit()
    if created:
        return f"{recipe.title} created.", 201
    else:
        return f"{recipe.title} modified.", 200


@bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.dictionary for c in categories])


@bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.filter_by(id=category_id).first_or_404()
    return jsonify(category.dictionary)


@bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.filter_by(id=category_id).first_or_404()
    category_repr = str(category)
    db.session.delete(category)
    db.session.commit()
    return f"{category_repr} deleted.", 200


@bp.route('/categories', methods=['POST'])
def post_category():
    data = request.json or request.form

    created = False

    if data.get("id"):
        category = Category.query.filter_by(id=data.get("id")).first_or_404()
    else:
        _assert_request_data(data, required=["name"])
        _validate_type(data["name"], str)
        category = Category(name=data["name"])
        created = True

    if data.get("name") and _validate_type(data.get("name"), str):
        category.name = data["name"]

    # tags
    tags = set()
    if data.get("tags") and _validate_type(data.get("tags"), list):
        for t in (data.get("tags") or []):
            tag_name = t.get("name")
            if not tag_name:
                continue
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            tags.add(tag)
    category.tags = list(tags)

    db.session.add(category)
    db.session.commit()
    if created:
        return f"{category.name} created.", 201
    else:
        return f"{category.name} modified.", 200
