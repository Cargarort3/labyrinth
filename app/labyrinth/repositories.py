from ..database import db
from .models import Labyrinth


class LabyrinthRepository:
    def get_by_id(id):
        return Labyrinth.query.filter_by(id=id).first()

    def get_by_userid(user_id):
        return Labyrinth.query.filter_by(user_id=user_id).all()

    def create(labyrinth):
        db.session.add(labyrinth)
        db.session.commit()
        return labyrinth

    def update(labyrinth):
        db.session.commit()
        return labyrinth

    def delete(id):
        labyrinth = Labyrinth.query.filter_by(id=id).first()
        db.session.delete(labyrinth)
        db.session.commit()
