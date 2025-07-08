from .repositories import AuthRepository
import math


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

    def get_best_users(self):
        users = self.authRepository.get_users_with_stats()

        def compute_score(user):
            stats = user.statistics
            perfect_win_rate = stats.precise_victories / stats.victories
            return perfect_win_rate * math.log(stats.victories + 1)

        ranked = sorted(users, key=compute_score, reverse=True)
        return ranked[:10]
