from .repositories import LabyrinthRepository


class LabyrinthService:

    def get_labyrinth_by_id(id):
        return LabyrinthRepository.get_by_id(id)

    def get_my_labyrinths(user_id):
        return LabyrinthRepository.get_by_userid(user_id)

    def create_labyrinth(labyrinth):
        return LabyrinthRepository.create(labyrinth)

    def delete_labyrinth(id):
        return LabyrinthRepository.delete(id)
