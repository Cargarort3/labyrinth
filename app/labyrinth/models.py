from ..database import db


class Labyrinth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    start = db.Column(db.String(5), nullable=False)
    end = db.Column(db.String(5), nullable=False)
    matrix = db.Column(db.JSON, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_published = db.Column(db.Boolean, default=False, nullable=False)

    def get_start(self):
        return tuple(map(int, self.start.split(',')))

    def get_end(self):
        return tuple(map(int, self.end.split(',')))

    def set_start(self, coor):
        self.start = f"{coor[0]},{coor[1]}"

    def set_end(self, coor):
        self.end = f"{coor[0]},{coor[1]}"
