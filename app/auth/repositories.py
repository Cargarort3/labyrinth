from ..database import db
from .models import User, Password, Statistics


class UserRepository:
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def get_by_id(id):
        return User.query.filter_by(id=id).first()

    def get_password_by_userid(user_id):
        return Password.query.filter_by(user_id=user_id).first()

    def create(username, password):
        new_statistics = Statistics(publications=0, victories=0, precise_victories=0)
        new_user = User(username=username, statistics=new_statistics)
        new_password = Password(user=new_user)
        new_password.set_password(password)
        db.session.add_all([new_statistics, new_user, new_password])
        db.session.commit()
        return new_user
