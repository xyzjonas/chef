import threading

from flask import current_app
from PIL import Image
import os


class Handler:

    THUMB = 96, 96
    SMALL = 540, 540
    MEDIUM = 768, 768

    SIZES = [
        ("thumb", THUMB),
        ("small", SMALL),
        ("medium", MEDIUM)
    ]

    def __init__(self, path, recipe_id) -> None:
        self.path = path
        self.recipe_id = recipe_id
        self.target = current_app.config["IMAGES_FOLDER"]

    def create_folder(self):
        if not os.path.isdir(self.target):
            raise Exception(f"No such fucking dir! {self.target}")

        recipe_folder = os.path.join(self.target, str(self.recipe_id))
        if not os.path.isdir(recipe_folder):
            os.mkdir(recipe_folder)

        return recipe_folder

    def create_images_set(self):
        image = Image.open(self.path)

        target_dir = self.create_folder()

        for name, size in self.SIZES:
            tmp_img = image.copy()
            tmp_img.thumbnail(size, Image.LANCZOS)
            tmp_img.save(os.path.join(target_dir, f"{name}.jpeg"))
