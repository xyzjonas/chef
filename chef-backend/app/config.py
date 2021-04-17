import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'hydro.db')
    IMAGES_FOLDER = "/var/www/html/chef/images"
    UPLOAD_FOLDER = "/tmp"


class TestConfig(Config):
    TEST = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
    IMAGES_FOLDER_PATH = "/tmp"
    UPLOAD_FOLDER = "/tmp"

    IMAGES_FOLDER = "/tmp"
