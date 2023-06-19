import os
from typing import Union

from pydantic import BaseSettings


class Settings(BaseSettings):
    serve_frontend: bool = False
    serve_frontend_path: str = "./src/js/chef/dist"
    database_uri: str = "sqlite:///chef.db"
    log_file: Union[str, None] = None
    log_level: str = "DEBUG"
    log_sql: bool = True

    upload_folder: str = "/tmp"  # temporary storage before processing
    images_folder: str = "/tmp/images"


settings = Settings()
