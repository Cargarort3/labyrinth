from .models import User
from ..database import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
