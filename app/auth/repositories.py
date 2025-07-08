from ..database import db
from .models import User, Password, Statistics


class AuthRepository:
    def get_by_username(self, username):
        return User.query.filter_by(username=username).first()

    def get_by_id(self, id):
        return User.query.filter_by(id=id).first()

    def get_password_by_userid(self, user_id):
        return Password.query.filter_by(user_id=user_id).first()

    def create(self, username, password):
        new_statistics = Statistics(publications=0, victories=0, precise_victories=0)
        new_user = User(username=username, statistics=new_statistics)
        new_password = Password(user=new_user)
        new_password.set_password(password)
        db.session.add_all([new_statistics, new_user, new_password])
        db.session.commit()
        return new_user

    def get_users_with_stats(self):
        return (
            db.session.query(User)
            .join(Statistics)
            .filter(Statistics.victories > 0)
            .all()
        )
