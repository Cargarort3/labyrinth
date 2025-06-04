from flask import Flask
from .config import Config
from .database import db, migrate, login_manager
from .main.routes import main
from .auth.routes import auth
from .labyrinth.routes import labyrinth


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(labyrinth)

    with app.app_context():
        db.create_all()

    return app
