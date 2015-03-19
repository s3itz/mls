import os


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['MLS_CONFIG_SECRET_KEY']
    DATABASE_URI = os.environ['MLS_CONFIG_DATABASE_URI']
    REDIS_URI = os.environ['MLS_CONFIG_REDIS_URI']


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False
