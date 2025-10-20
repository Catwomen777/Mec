from flask import Flask
from app.extensions import db, ma, limiter, cache
from app.models import db

def create_app(config_name):
    
    app = Flask(__name__)
    app.config.from_object(f'congfig.{config_name}')
    
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
     # Import models before creating tables
    from . import models  # noqa

    
    from .blueprints.customers import customers_bp
    from .blueprints.mechanics import mechanics_bp
    from .blueprints.servicetickets import service_tickets_bp4
    from .blueprints.inventory import inventory_bp

    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    with app.app_context():
        db.create_all()

    return app
    
    
    
    
    
    
    return app