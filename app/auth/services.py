from .repositories import AuthRepository


class AuthService:
    def __init__(self):
        self.authRepository = AuthRepository()

    def register_user(self, username, password):
        if self.authRepository.get_by_username(username):
            return None
        return self.authRepository.create(username, password)

    def authenticate_user(self, username, password):
        user = self.authRepository.get_by_username(username)
        if user:
            passw = self.authRepository.get_password_by_userid(user.id)
            if passw.check_password(password):
                return user
        return None

    def get_user_by_id(self, id):
        return self.authRepository.get_by_id(id)
