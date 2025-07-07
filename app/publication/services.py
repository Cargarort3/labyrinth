from .repositories import PublicationRepository


class PublicationService:
    def __init__(self):
        self.publicationRepository = PublicationRepository()

    def get_all_publications(self):
        return self.publicationRepository.get_all()

    def get_publication_by_id(self, id):
        return self.publicationRepository.get_by_id(id)

    def get_user_publications(self, user_id):
        return self.publicationRepository.get_by_userid(user_id)

    def create_publication(self, publication, labyrinth):
        return self.publicationRepository.create(publication, labyrinth)

    def add_publication_winner(self, id, winner, perfect):
        return self.publicationRepository.add_winner(id, winner, perfect)
