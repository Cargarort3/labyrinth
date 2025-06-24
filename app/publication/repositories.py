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
        db.session.add(publication)
        db.session.commit()
        return publication
