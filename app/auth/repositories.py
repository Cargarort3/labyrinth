from ..database import db
from .models import User


class UserRepository:
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def create(username, password):
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user
