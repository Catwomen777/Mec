from flask import Flask
from flask_limiter.util import get_remote_address
from app.extensions import db, ma, cache, limiter
from app.blueprints.customers import customers_bp
from app.blueprints.mechanics import mechanics_bp
from app.blueprints.servicetickets import service_tickets_bp
from app.blueprints.inventory import inventory_bp


# --- Initialize extensions globally ---


def create_app(config_name="DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name}")

    # --- Initialize extensions ---
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)

    # --- Register blueprints ---
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service_tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    # --- Create database tables ---
    with app.app_context():
         db.create_all()
         DEBUG = True
        
    print("URL MAP:\n", app.url_map)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
    

