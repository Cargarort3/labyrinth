from ..database import db
from .models import Publication
from app.labyrinth.models import Labyrinth


class PublicationRepository:
    def get_all(self):
        return Publication.query.all()

    def get_by_id(self, id):
        return Publication.query.filter_by(id=id).first()

    def get_by_userid(self, user_id):
        return (Publication.query.join(Labyrinth).filter(Labyrinth.user_id == user_id).all())

    def create(self, publication, labyrinth):
        labyrinth.is_published = True
        db.session.add(labyrinth)
        statistics = labyrinth.user.statistics
        statistics.publications += 1
        db.session.add(statistics)
        db.session.add(publication)
        db.session.commit()
        return publication

    def add_winner(self, id, winner, perfect):
        publication = Publication.query.filter_by(id=id).first()
        publication.winners.append(winner)
        db.session.add(publication)
        statistics = winner.statistics
        statistics.victories += 1
        if perfect:
            statistics.precise_victories += 1
        db.session.commit()
