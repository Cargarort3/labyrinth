from ..database import db
from .models import Labyrinth


class LabyrinthRepository:
    def get_by_id(self, id):
        return Labyrinth.query.filter_by(id=id).first()

    def get_by_userid(self, user_id):
        return Labyrinth.query.filter_by(user_id=user_id).all()

    def create(self, labyrinth):
        db.session.add(labyrinth)
        db.session.commit()
        return labyrinth

    def update(self, labyrinth):
        db.session.commit()
        return labyrinth

    def delete(self, id):
        labyrinth = Labyrinth.query.filter_by(id=id).first()
        db.session.delete(labyrinth)
        db.session.commit()
