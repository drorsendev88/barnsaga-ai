from flask import Flask
from app.routes.input_routes import input_routes
from app.routes.generate_routes import generate_routes
from app.routes.health_routes import health_routes

def create_app():
    app = Flask(__name__)

    # Registrera Blueprints
    app.register_blueprint(input_routes)
    app.register_blueprint(generate_routes)
    app.register_blueprint(health_routes)

    return app
