import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

SCAN_SLEEP = 2

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)

    if os.environ.get('CHEF_CONFIG'):
        app.config.from_envvar('CHEF_CONFIG')
    else:
        print("Config loaded from a .py file, set 'CHEF_CONFIG' variable to use a config file.")
        app.config.from_object(config_class)

    if app.config.get("LOG_FILE"):
        log_format = '[%(asctime)s] %(levelname)s\t[%(name)s] %(message)s'
        file_handler = logging.FileHandler(filename=app.config['LOG_FILE'], mode='a')
        file_handler.setFormatter(logging.Formatter(log_format))
        app.logger.addHandler(file_handler)

    app.logger.info("""
    ██████╗██╗  ██╗███████╗███████╗
    ██╔════╝██║  ██║██╔════╝██╔════╝
    ██║     ███████║█████╗  █████╗  
    ██║     ██╔══██║██╔══╝  ██╔══╝  
    ╚██████╗██║  ██║███████╗██║     
    ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝
""")

    database_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    db.init_app(app)
    db.app = app

    # Log some useful setup info
    app.logger.info(f"DB: {database_uri} initialized")
    app.logger.info(f"Logging to: {app.config.get('LOG_FILE', None)}")
    app.logger.info(f"Storing temp files at: {app.config.get('UPLOAD_FOLDER', None)}")
    app.logger.info(f"Serving images from: {app.config.get('IMAGES_FOLDER', None)}")

    is_sqlite = database_uri.startswith('sqlite:')
    migrate.init_app(app, db, render_as_batch=is_sqlite)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.image import bp as image_bp
    app.register_blueprint(image_bp)

    if not app.debug and not app.testing:
        # ... no changes to logging setup
        pass

    CORS(app, resources={r'/*': {'origins': '*'}})
    return app
