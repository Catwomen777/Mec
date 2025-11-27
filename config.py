import os


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    DEBUG = True
    CACHE_TYPE = "SimpleCache"

class TestingConfig:
    TESTING = True
    DEBUG = True
    SECRET_KEY = "test-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    CACHE_TYPE = "simple"

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")or 'sqlite:///app.db'
    Cache_TYPE = "SimpleCache"