from flask import Flask
import os
from dotenv import load_dotenv

from .service.database import db


def create_app(type):
    load_dotenv(dotenv_path=".env")
    app = Flask(__name__, template_folder='templates')

    if type == "test":
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        constring = 'sqlite:///:memory:'
    else:
        constring = os.getenv("CON_STRING")

    app.config["SECRET_KEY"] = os.getenv("KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = constring
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


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
