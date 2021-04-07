import logging

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import Config


SCAN_SLEEP = 2

db = SQLAlchemy()
migrate = Migrate()

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')
log = logging.getLogger(__name__)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    db.app = app
    migrate.init_app(app, db)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        # ... no changes to logging setup
        pass

    CORS(app, resources={r'/*': {'origins': '*'}})
    return app
