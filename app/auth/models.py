from ..database import db
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

bcrypt = Bcrypt()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    labyrinths = db.relationship('Labyrinth', backref='user', lazy=True)
    statistics = db.relationship('Statistics', lazy=True, uselist=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publications = db.Column(db.Integer, nullable=False)
    victories = db.Column(db.Integer, nullable=False)
    precise_victories = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
