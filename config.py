import os


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    DEBUG = True
    SECRET_KEY = "your_secret_key"
    
    
    
class TestingConfig:
    TESTING = True
    SECRET_KEY = "testing_secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"   # Fast, isolated DB for tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get(SQLALCHEMY_DATABASE_URI) or 'sqlite:///app.db'
    CACHE_TYPE = "SimpleCache"  # Use a more robust cache in production