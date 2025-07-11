from flask import Flask
from .config import Config, TestingConfig, DeploymentConfig
from .database import db, login_manager
from .main.routes import main
from .auth.routes import auth
from .labyrinth.routes import labyrinth
from .publication.routes import publication


def create_app(config_name=None):
    app = Flask(__name__)
    if config_name == 'testing':
        app.config.from_object(TestingConfig)
    elif config_name == 'deployment':
        app.config.from_object(DeploymentConfig)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(labyrinth)
    app.register_blueprint(publication)

    with app.app_context():
        db.create_all()

    return app
