import os
from flask import jsonify, request, current_app
from datetime import datetime

from app.exceptions import InvalidUsage
from app.image import bp
from app.image.handler import Handler
from app.models import Recipe


@bp.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@bp.route('/recipes/<int:recipe_id>/image', methods=['POST'])
def post_image(recipe_id):
    Recipe.query.filter_by(id=recipe_id).first_or_404()
    image = request.files.get("image")
    if not image:
        raise InvalidUsage("No 'image' uploaded.")

    upload_path = current_app.config["UPLOAD_FOLDER"]
    if not os.path.isdir(upload_path):
        raise InvalidUsage("Server misconfiguration, invalid images path.", status_code=500)

    image_dir_name = f"chef_upload_{datetime.utcnow().timestamp()}"
    os.mkdir(os.path.join(upload_path, image_dir_name))

    image_path = os.path.join(upload_path, image_dir_name, image.filename)
    image.save(image_path)

    handler = Handler(image_path, recipe_id)
    handler.create_images_set()

    return f"Images sent for processing...", 200
