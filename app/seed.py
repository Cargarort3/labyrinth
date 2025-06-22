from app.database import db
from app.auth.models import User
from app.labyrinth.models import Labyrinth
from app import create_app

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Users
    user1 = User(username="user1")
    user1.set_password("complexpass")
    user2 = User(username="user2")
    user2.set_password("complexpass")
    db.session.add_all([user1, user2])

    # Labyrinths
    m = [[0, 1, 0, 0, 0], [0, 0, 0, 1, 0], [1, 0, 1, 1, 0], [1, 0, 1, 1, 0], [1, 0, 0, 0, 0]]
    lab1 = Labyrinth(title="Lab A", description="Simple labyrinth", matrix=m, start="1,1", end="5,5", user=user1)
    lab2 = Labyrinth(title="Lab B", description="Simple labyrinth", matrix=m, start="1,1", end="5,5", user=user2)
    db.session.add_all([lab1, lab2])

    db.session.commit()
