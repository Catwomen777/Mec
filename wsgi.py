from app import create_app
from app.models import db

def app():
    flask_app = create_app('ProductionConfig')
    with flask_app.app_context():
        db.create_all()
    return flask_app
