from flask import Flask
from app.extensions import db, ma, limiter, cache
from flask_swagger_ui import get_swaggerui_blueprint
from .main import create_app



SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml'  # Our API URL (can of course be a local resource)

swagger_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Mechanic Shop API"}
        
)



def create_app(config_name="ProductionConfig"):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name}")
    
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    limiter.exempt(swagger_bp)
    limiter.exempt(app.view_functions['static'])

    
    
    from . import models  

    
    from .blueprints.customers import customers_bp
    from .blueprints.mechanics import mechanics_bp
    from .blueprints.servicetickets import service_tickets_bp
    from .blueprints.inventory import inventory_bp

    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL) #Registering our swagger blueprint

    with app.app_context():
        db.drop_all()
        db.create_all()
        
        print("\n🚀 REGISTERED ROUTES:")
        for rule in app.url_map.iter_rules():
            
            
            return app
    