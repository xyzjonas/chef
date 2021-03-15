from flask import jsonify, request

from app import db
from app.main import bp
from app.models import Recipe


@bp.route('/', methods=['GET'])
def root():
    return "Hello world!", 200


@bp.route('/recipes', methods=['GET'])
def recipes_get():
    recipes = [recipe.dictionary for recipe in Recipe.query.all()]
    return jsonify(recipes), 200


@bp.route('/recipes/<int:recipe_id>', methods=['GET'])
def recipes_get_single(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    return jsonify(recipe.dictionary), 200


@bp.route('/recipes/<int:recipe_id>/text', methods=['GET'])
def recipes_get_body(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    return str(recipe.body), 200


@bp.route('/recipes/<int:recipe_id>/text', methods=['POST'])
def recipes_upload_body(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first_or_404()
    data = request.json or request.form
    if not data:
        return "No data received.", 400
    if not data.get("text"):
        return "'text' field is required.", 400

    recipe.body = data["text"]
    db.session.add(recipe)
    db.session.commit()
    return f"{recipe} modified", 200
