from .repositories import UserRepository


class AuthService:
    def register_user(username, password):
        if UserRepository.get_by_username(username):
            return None
        return UserRepository.create(username, password)

    def authenticate_user(username, password):
        user = UserRepository.get_by_username(username)
        if user and user.check_password(password):
            return user
        return None
