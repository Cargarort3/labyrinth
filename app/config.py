import os


class Config:
    DB_USERNAME = "labyrinth_user"
    DB_PASSWORD = "labyrinth_password"
    DB_HOST = "localhost"
    DB_NAME = "labyrinth_db"

    SQLALCHEMY_DATABASE_URI = f"mariadb+mariadbconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)


class TestingConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test-secret"
