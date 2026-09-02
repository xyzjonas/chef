import os
from datetime import datetime

from fastapi import APIRouter, HTTPException

from chef.settings import settings

router = APIRouter()


def _create_tmp_dir():
    upload_path = settings.upload_folder
    if not os.path.isdir(upload_path):
        raise HTTPException(status_code=500, detail="Server misconfiguration, invalid images path.")

    image_dir_name = f"chef_upload_{datetime.utcnow().timestamp()}"
    path = os.path.join(upload_path, image_dir_name)
    os.mkdir(path)
    return path


# @router.post('/recipes/{recipe_id}')
# async def post_recipe_image(recipe_id: int, image: UploadFile):
#     await generic_get(recipes, recipe_id)
#     logger.debug(f"uploading recipe (id={recipe_id}) image: {image.filename}, {image.size}b")
#
#     handler = Handler(image.file, recipe_id)
#     handler.create_images_set()
#
#     return f"Recipe images sent for processing...", 200
