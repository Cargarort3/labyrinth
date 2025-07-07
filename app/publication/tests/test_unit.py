import pytest
import json
from app.auth.repositories import AuthRepository


@pytest.mark.unit
class TestPublication:
    def setup_method(self):
        self.authRepository = AuthRepository()

    def login(self, client, username="example", password="password"):
        if not self.authRepository.get_by_username(username):
            self.authRepository.create(username, password)

        return client.post('/login', data={
            "username": username,
            "password": password
        }, follow_redirects=True)

    def test_publications_screen(self, client):
        response = client.get('/publication/')
        assert response.status_code == 200
        assert b"All publicated labyrinths" in response.data

        response = client.get('/publication/1')
        assert response.status_code == 404
        assert b"Publication not found" in response.data

    def test_publish_labyrinth(self, client):
        self.login(client)

        data = {
            "title": "Test Labyrinth",
            "description": "Simple description",
            "labyrinth": [
                [0, 1, 0, 1, 0],
                [0, 0, 0, 1, 0],
                [1, 0, 1, 1, 0],
                [1, 0, 1, 1, 0],
                [1, 0, 0, 0, 0],
            ],
            "start": [1, 1],
            "end": [5, 5]
        }
        client.post('/labyrinth/create', data=json.dumps(data), content_type='application/json')

        response = client.post('/publication/create/1', follow_redirects=True)
        assert response.status_code == 200
        assert b"Test Labyrinth" in response.data

        response = client.get('/publication/1')
        assert response.status_code == 200
        assert b"Test Labyrinth" in response.data

    def test_publish_labyrinth_wrong(self, client):
        self.login(client)

        data = {
            "title": "Test Labyrinth",
            "description": "Simple description",
            "labyrinth": [
                [0, 1, 0, 1, 0],
                [0, 0, 0, 1, 0],
                [1, 0, 1, 1, 0],
                [1, 0, 1, 1, 0],
                [1, 0, 1, 0, 0],
            ],
            "start": [1, 1],
            "end": [5, 5]
        }

        client.post('/labyrinth/create', data=json.dumps(data), content_type='application/json')
        response = client.post('/publication/create/1')
        assert response.status_code == 400
        assert response.is_json
        assert response.get_json() == {"error": "Your labyrinth has no solution."}

        response = client.post('/publication/create/2')
        assert response.status_code == 404
        assert b"Labyrinth not found" in response.data

        data["labyrinth"] = [
            [0, 1, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [1, 0, 1, 1, 0],
            [1, 0, 1, 1, 0],
            [1, 0, 0, 0, 0],
        ]
        client.post('/labyrinth/edit/1', data=json.dumps(data), content_type='application/json')

        client.get('/logout')
        self.login(client, "example2")
        response = client.post('/publication/create/1')
        assert response.status_code == 401
        assert b"You don't have permission" in response.data

        client.post('/labyrinth/create', data=json.dumps(data), content_type='application/json')
        client.post('/publication/create/2')
        response = client.post('/publication/create/2')
        assert response.status_code == 400
        assert b"This labyrinth is already published" in response.data

    def test_immutable_publication(self, client):
        self.login(client)

        data = {
            "title": "Test Labyrinth",
            "description": "Simple description",
            "labyrinth": [
                [0, 1, 0, 1, 0],
                [0, 0, 0, 1, 0],
                [1, 0, 1, 1, 0],
                [1, 0, 1, 1, 0],
                [1, 0, 0, 0, 0],
            ],
            "start": [1, 1],
            "end": [5, 5]
        }

        client.post('/labyrinth/create', data=json.dumps(data), content_type='application/json')
        client.post('/publication/create/1')

        response = client.post('/labyrinth/edit/1', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert b"You can't edit a published labyrinth" in response.data

        response = client.delete('/labyrinth/1')
        assert response.status_code == 400
        assert b"You can't delete a published labyrinth" in response.data

    def test_solve_publication(self, client):
        self.login(client)

        data = {
            "title": "Test Labyrinth",
            "description": "Simple description",
            "labyrinth": [
                [0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0],
                [1, 0, 1, 1, 0],
                [1, 0, 1, 1, 0],
                [1, 0, 0, 0, 0],
            ],
            "start": [1, 1],
            "end": [5, 5]
        }

        client.post('/labyrinth/create', data=json.dumps(data), content_type='application/json')
        client.post('/publication/create/1')

        client.get('/logout')
        self.login(client, "example2")
        data = {
            "path": ["1,1", "2,1", "2,2", "3,2", "4,2", "5,2", "5,3", "5,4", "5,5"]
        }
        response = client.post('/publication/solve/1', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert response.is_json
        assert response.get_json() == {"result": "Valid solution in 8 steps, best solution in 8 steps"}

        client.get('/logout')
        self.login(client, "example3")
        data = {
            "path": ["1,1", "2,1", "2,2", "2,3", "1,3", "1,4", "1,5", "2,5", "3,5", "4,5", "5,5"]
        }
        response = client.post('/publication/solve/1', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert response.is_json
        assert response.get_json() == {"result": "Valid solution in 10 steps, best solution in 8 steps"}

    def test_solve_publication_wrong(self, client):
        self.login(client)

        data = {
            "title": "Test Labyrinth",
            "description": "Simple description",
            "labyrinth": [
                [0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0],
                [1, 0, 1, 1, 0],
                [1, 0, 1, 1, 0],
                [1, 0, 0, 0, 0],
            ],
            "start": [1, 1],
            "end": [5, 5]
        }

        client.post('/labyrinth/create', data=json.dumps(data), content_type='application/json')
        client.post('/publication/create/1')

        data = {
            "path": ["1,1", "2,1", "2,2", "3,2", "4,2", "5,2", "5,3", "5,4"]
        }
        response = client.post('/publication/solve/1', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert response.is_json
        assert response.get_json() == {"result": "Solution not valid"}

        data = {
            "path": ["1,1", "2,1", "3,1", "3,2", "4,2", "5,2", "5,3", "5,4", "5,5"]
        }
        response = client.post('/publication/solve/1', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert response.is_json
        assert response.get_json() == {"result": "Solution not valid"}

        response = client.post('/publication/solve/2', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 404
        assert b"Publication not found" in response.data
