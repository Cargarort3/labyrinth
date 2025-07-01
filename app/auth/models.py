from ..database import db
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    labyrinths = db.relationship('Labyrinth', backref='user', lazy=True)
    statistics = db.relationship('Statistics', lazy=True, uselist=False)


class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(255), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    user = db.relationship('User', lazy=True, uselist=False)

    def set_password(self, password):
        self.hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.hash, password)


class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publications = db.Column(db.Integer, nullable=False)
    victories = db.Column(db.Integer, nullable=False)
    precise_victories = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
