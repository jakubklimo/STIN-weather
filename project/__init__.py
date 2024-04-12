from flask import Flask
import os
from dotenv import load_dotenv

from .service.database import db


def create_app():
    app = Flask(__name__, template_folder='templates')

    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)

    db.init_app(app)

    register_blueprints(app)

    with app.app_context():
        db.create_all()



    return app

def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from project.controllers.main_controller import main_bp
    from project.controllers.user_controller import user_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
