import random
from app.database import db
from app.auth.models import User, Password, Statistics
from app.labyrinth.models import Labyrinth
from app.publication.models import Publication
from app import create_app

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    users = []
    stats_map = {}

    for i in range(1, 16):
        stats = Statistics(publications=0, victories=0, precise_victories=0)
        user = User(username=f"user{i}", statistics=stats)
        pw = Password(user=user)
        pw.set_password("complexpass")
        db.session.add_all([stats, user, pw])
        users.append(user)
        stats_map[user.username] = stats

    db.session.flush()

    m = [
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [1, 0, 1, 1, 0],
        [1, 0, 1, 1, 0],
        [1, 0, 0, 0, 0]
    ]

    publication_count = 20
    author_cycle = users[:5]

    for i in range(publication_count):
        author = author_cycle[i % len(author_cycle)]
        stats_map[author.username].publications += 1

        lab = Labyrinth(
            title=f"Lab {i+1}",
            description=f"Generated labyrinth {i+1}",
            matrix=m,
            start="1,1",
            end="5,5",
            user=author,
            is_published=True
        )

        pub = Publication(
            labyrinth=lab,
            min_movements=8 + (i % 5)
        )

        eligible_winners = [u for u in users if u != author]

        if i == 0:
            selected_winners = []
        else:
            max_winners = min(10, len(eligible_winners))
            num_winners = random.randint(1, max_winners)
            selected_winners = random.sample(eligible_winners, k=num_winners)

        for winner in selected_winners:
            pub.winners.append(winner)
            stats = stats_map[winner.username]
            stats.victories += 1

            if random.random() < 0.6:
                stats.precise_victories += 1

        db.session.add_all([lab, pub])

    db.session.commit()
