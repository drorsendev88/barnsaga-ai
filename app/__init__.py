from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Ladda konfigurationen från config.py
    app.config.from_object("app.config.Config")

    # Importera routes
    from app.routes import main
    app.register_blueprint(main)

    return app