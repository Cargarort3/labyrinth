from ..database import db
from datetime import datetime, timezone


class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posted_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    max_movements = db.Column(db.Integer)

    labyrinth_id = db.Column(db.Integer, db.ForeignKey('labyrinth.id'), nullable=False, unique=True)
    labyrinth = db.relationship('Labyrinth', lazy=True, uselist=False)
