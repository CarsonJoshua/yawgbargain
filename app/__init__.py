from flask import Flask
from .config import Config
from .dao import db  # Import db from extensions.py

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints (modularized routes)
    from .routes import index_bp
    from .routes import card_price_bp
    from .routes import pricer_bp
    from .routes import release_notes_bp
    
    app.register_blueprint(index_bp)
    app.register_blueprint(card_price_bp)
    app.register_blueprint(pricer_bp)
    app.register_blueprint(release_notes_bp)

    return app
