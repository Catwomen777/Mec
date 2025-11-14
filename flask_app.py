from app import create_app
from app.models import db



def create_app(config_name="ProductiontConfig"):
     app = create_app(config_name)
     return app
