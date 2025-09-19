from .repositories import LabyrinthRepository


class LabyrinthService:
    def __init__(self):
        self.labyrinthRepository = LabyrinthRepository()

    def get_labyrinth_by_id(self, id):
        return self.labyrinthRepository.get_by_id(id)

    def get_my_labyrinths_paginated(self, user_id, page: int, per_page: int):
        labyrinths = self.labyrinthRepository.get_by_userid(user_id)[::-1]
        total = len(labyrinths)

        start = (page - 1) * per_page
        end = start + per_page
        return labyrinths[start:end], total

    def create_labyrinth(self, labyrinth):
        return self.labyrinthRepository.create(labyrinth)

    def update_labyrinth(self, labyrinth):
        return self.labyrinthRepository.update(labyrinth)

    def delete_labyrinth(self, id):
        return self.labyrinthRepository.delete(id)
