import os.path
from pathlib import Path
from typing import Union

from pydantic import BaseSettings

HOME_DIR = Path.home() / '.chef'


class Settings(BaseSettings):
    """Default config will store all user data in ~/.chef"""
    serve_frontend: bool = False
    serve_frontend_path: str = "./src/js/chef/dist"
    database_uri: str = "sqlite:///" + os.path.join(HOME_DIR,  "chef.db")
    log_file: Union[str, None] = None
    log_level: str = "DEBUG"
    log_sql: bool = False

    images_folder: str = os.path.join(HOME_DIR,  "images")

    uvicorn_host: str = "0.0.0.0"
    uvicorn_port: int = 8000


settings = Settings()
