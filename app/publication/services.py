from .repositories import PublicationRepository


class PublicationService:
    def __init__(self):
        self.publicationRepository = PublicationRepository()

    def get_all_publications_paginated(self, page: int, per_page: int):
        publications = self.publicationRepository.get_all()[::-1]
        total = len(publications)

        start = (page - 1) * per_page
        end = start + per_page
        return publications[start:end], total

    def get_publication_by_id(self, id):
        return self.publicationRepository.get_by_id(id)

    def get_user_publications_paginated(self, user_id, page: int, per_page: int):
        publications = self.publicationRepository.get_by_userid(user_id)[::-1]
        total = len(publications)

        start = (page - 1) * per_page
        end = start + per_page
        return publications[start:end], total

    def create_publication(self, publication, labyrinth):
        return self.publicationRepository.create(publication, labyrinth)

    def add_publication_winner(self, id, winner, perfect):
        return self.publicationRepository.add_winner(id, winner, perfect)

    def get_most_popular_publications(self):
        publications = self.publicationRepository.get_all()
        publications.sort(key=lambda p: len(p.winners), reverse=True)
        return publications[:10]
