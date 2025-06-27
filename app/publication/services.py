from .repositories import PublicationRepository


class PublicationService:

    def get_all_publications():
        return PublicationRepository.get_all()

    def get_publication_by_id(id):
        return PublicationRepository.get_by_id(id)

    def create_publication(publication, labyrinth):
        return PublicationRepository.create(publication, labyrinth)

    def add_publication_winner(id, winner, perfect):
        return PublicationRepository.add_winner(id, winner, perfect)
