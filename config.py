import os


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    DEBUG = True
    CACHE_TYPE = "SimpleCache"

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    TESTING: True
    Debug = True
    SECRET_KEY = "test-secret-key"
    CACHE_TYPE = "simpleCache"

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")or 'sqlite:///app.db'
    Cache_TYPE = "SimpleCache"