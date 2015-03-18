import os


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['MLS_CONFIG_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['MLS_CONFIG_DATABASE_URI']


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass