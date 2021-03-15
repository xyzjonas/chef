import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'hydro.db')


class TestConfig(Config):
    TEST = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"