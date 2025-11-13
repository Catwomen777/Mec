from flask import Flask
from flask_limiter.util import get_remote_address
from app.extensions import db, ma, cache, limiter
from app.blueprints.customers import customers_bp
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.servicetickets import service_tickets_bp
from app.blueprints.inventory import inventory_bp
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swagger_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Auto Shop API"}
)


def create_app(config_name="ProductionConfig"):
    app = Flask(
    __name__,
    static_url_path='/static',
    static_folder='static'
)

    app.config.from_object(f"config.{config_name}")

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    limiter.exempt(swagger_bp)

    # Register blueprints
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

    # Create database tables
    with app.app_context():
        db.create_all()

    print("URL MAP:\n", app.url_map)
    return app


# ✅ This ensures both local and Render deployments work
app = create_app("ProductionConfig")

if __name__ == "__main__":
    app.run(debug=True)
