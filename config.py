class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    DEBUG = True
    SECRET_KEY = "your_secret_key"
    
    
    
class TestingConfig:
    TESTING = True
    SECRET_KEY = "testing_secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"   # Fast, isolated DB for tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False
