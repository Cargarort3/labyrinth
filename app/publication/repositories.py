from ..database import db
from .models import Publication


class PublicationRepository:
    def get_all():
        return Publication.query.all()

    def get_by_id(id):
        return Publication.query.filter_by(id=id).first()

    def create(publication, labyrinth):
        labyrinth.is_published = True
        db.session.add(labyrinth)
        statistics = labyrinth.user.statistics
        statistics.publications += 1
        db.session.add(statistics)
        db.session.add(publication)
        db.session.commit()
        return publication

    def add_winner(id, winner, perfect):
        publication = Publication.query.filter_by(id=id).first()
        publication.winners.append(winner)
        db.session.add(publication)
        statistics = winner.statistics
        statistics.victories += 1
        if perfect:
            statistics.precise_victories += 1
        db.session.commit()
