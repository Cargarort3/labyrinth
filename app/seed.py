from app.database import db
from app.auth.models import User, Password, Statistics
from app.labyrinth.models import Labyrinth
from app.publication.models import Publication
from app import create_app

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Users
    statistics1 = Statistics(publications=0, victories=0, precise_victories=0)
    user1 = User(username="user1", statistics=statistics1)
    pass1 = Password(user=user1)
    pass1.set_password("complexpass")
    statistics2 = Statistics(publications=0, victories=0, precise_victories=0)
    user2 = User(username="user2", statistics=statistics2)
    pass2 = Password(user=user2)
    pass2.set_password("complexpass")
    db.session.add_all([statistics1, user1, pass1, statistics2, user2, pass2])

    # Labyrinths
    m = [[0, 1, 0, 0, 0], [0, 0, 0, 1, 0], [1, 0, 1, 1, 0], [1, 0, 1, 1, 0], [1, 0, 0, 0, 0]]
    lab1 = Labyrinth(title="Lab A", description="Simple labyrinth", matrix=m, start="1,1", end="5,5", user=user1)
    lab2 = Labyrinth(title="Lab B", description="Simple labyrinth", matrix=m, start="1,1", end="5,5", user=user2, is_published=True)
    pub2 = Publication(min_movements=8, labyrinth=lab2)
    db.session.add_all([lab1, lab2, pub2])

    db.session.commit()
