import os


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    DEBUG = True
    CACHE_TYPE = "SimpleCache"

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    Debug = True
    CACHE_TYPE = "simpleCache"

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    Cache_TYPE = "SimpleCache"