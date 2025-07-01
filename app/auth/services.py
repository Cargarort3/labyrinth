from .repositories import UserRepository


class AuthService:
    def register_user(username, password):
        if UserRepository.get_by_username(username):
            return None
        return UserRepository.create(username, password)

    def authenticate_user(username, password):
        user = UserRepository.get_by_username(username)
        if user:
            passw = UserRepository.get_password_by_userid(user.id)
            if passw.check_password(password):
                return user
        return None

    def get_user_by_id(id):
        return UserRepository.get_by_id(id)
