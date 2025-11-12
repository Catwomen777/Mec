import os


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    DEBUG = True
    SECRET_KEY = "your_secret_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig:
    TESTING = True
    SECRET_KEY = "testing_secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"   # Fast, isolated DB for tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig:
    # ✅ FIXED — added quotes around environment variable name
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///app.db")
    SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "SimpleCache"  # Use a more robust cache in production
