import pytest
import json
from app.auth.repositories import AuthRepository
from app.labyrinth.algorithms import bfs, matrix_to_graph


@pytest.mark.unit
class TestLabyrinth():
    def setup_method(self):
        self.authRepository = AuthRepository()

    def login(self, client, username="example", password="password"):
        if not self.authRepository.get_by_username(username):
            self.authRepository.create(username, password)

        return client.post('/login', data={
            "username": username,
            "password": password
        }, follow_redirects=True)

    def test_labyrinth_screens(self, client):
        response = client.get('/labyrinth/create')
        assert response.status_code == 200
        assert b"Introduce the labyrinth" in response.data

        self.login(client)
        response = client.get('/labyrinth/')
        assert response.status_code == 200
        assert b"My labyrinths" in response.data

    def test_solve_labyrinth_success(self, client):
        data = {
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

        response = client.post('/labyrinth/solve', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        result = response.get_json()
        assert len(result["path"]) == 9
        assert result["path"][2] == [[2, 2], "🡇"]
        assert result["path"][-1] == [[5, 5], "🚩"]

        data["algorithm"] = "dfs"
        response = client.post('/labyrinth/solve', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        result = response.get_json()
        assert len(result["path"]) == 11
        assert result["path"][2] == [[2, 2], "🡆"]
        assert result["path"][-1] == [[5, 5], "🚩"]

        data["algorithm"] = "rw"
        response = client.post('/labyrinth/solve', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        result = response.get_json()
        assert len(result["path"]) >= 9
        assert result["path"][0] == [[1, 1], "🡇"]
        assert result["path"][-1] == [[5, 5], "🚩"]
        response = client.get('/register')
        assert response.status_code == 200
        assert b"Register" in response.data

    def test_solve_labyrinth_no_solution(self, client):
        data = {
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

        response = client.post('/labyrinth/solve', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        result = response.get_json()
        assert result["path"] is None

        data["algorithm"] = "dfs"
        response = client.post('/labyrinth/solve', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        result = response.get_json()
        assert result["path"] is None

        data["algorithm"] = "rw"
        response = client.post('/labyrinth/solve', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        result = response.get_json()
        assert result["path"] is None

    def test_create_and_delete_labyrinth(self, client):
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

        response = client.post('/labyrinth/create', data=json.dumps(data), content_type='application/json', follow_redirects=True)
        assert response.status_code == 200
        assert b"Test Labyrinth" in response.data

        response = client.get('/labyrinth/1')
        assert response.status_code == 200
        assert b"Test Labyrinth" in response.data

        client.get('/logout')
        self.login(client, "example2")
        response = client.get('/labyrinth/1')
        assert response.status_code == 401
        assert b"You don't have permission" in response.data

        response = client.delete('/labyrinth/1')
        assert response.status_code == 401
        assert b"You don't have permission" in response.data

        client.get('/logout')
        self.login(client)
        response = client.delete('/labyrinth/1')
        assert response.status_code == 200
        assert response.data == b"Labyrinth deleted"

        response = client.get('/labyrinth/')
        assert response.status_code == 200
        assert b"No labyrinths found" in response.data

        response = client.delete('/labyrinth/1')
        assert response.status_code == 404
        assert b"Labyrinth not found" in response.data

        response = client.get('/labyrinth/1')
        assert response.status_code == 404
        assert b"Labyrinth not found" in response.data

    def test_edit_labyrinth(self, client):
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
        client.post('/labyrinth/create', data=json.dumps(data), content_type='application/json', follow_redirects=True)

        response = client.get('/labyrinth/edit/1')
        assert response.status_code == 200
        assert b"Test Labyrinth" in response.data

        data = {
            "title": "Edited Labyrinth",
            "description": "Better description",
            "labyrinth": [
                [0, 1, 0, 1, 0, 1],
                [0, 0, 0, 1, 0, 1],
                [1, 0, 1, 1, 0, 1],
                [1, 0, 1, 1, 0, 1],
                [1, 0, 1, 0, 0, 0],
            ],
            "start": [1, 1],
            "end": [5, 6]
        }
        response = client.post('/labyrinth/edit/1', data=json.dumps(data), content_type='application/json', follow_redirects=True)
        assert response.status_code == 200
        assert b"Edited Labyrinth" in response.data
        assert b"Better description" in response.data

        client.get('/logout')
        self.login(client, "example2")
        response = client.get('/labyrinth/edit/1')
        assert response.status_code == 401
        assert b"You don't have permission" in response.data

        response = client.get('/labyrinth/edit/2')
        assert response.status_code == 404
        assert b"Labyrinth not found" in response.data

    def test_create_and_edit_labyrinth_wrong(self, client):
        self.login(client)

        data = {
            "title": "",
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

        response = client.post('/labyrinth/create', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert response.is_json
        assert response.get_json() == {"error": "Title is required"}

        data["title"] = "Test Labyrinth"
        data["end"] = [6, 5]
        response = client.post('/labyrinth/create', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert b"Start and end coordinates are out of bounds" in response.data

        data["end"] = [5, 4]
        data["labyrinth"] = [
            [0, 1, 0, 1],
            [0, 0, 0, 1],
            [1, 0, 1, 1],
            [1, 0, 1, 1],
            [1, 0, 1, 0],
        ]
        response = client.post('/labyrinth/create', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert b"Labyrinth dimensions must be between 5x5 and 30x50" in response.data

        data["labyrinth"] = [
            [0, 1, 0, 1, 0],
            [0, 0, 0, 1, 0],
            [1, 0, 1, 1, 0],
            [1, 0, 1, 1, 0],
            [1, 0, 1, 0, 0],
        ]
        client.post('/labyrinth/create', data=json.dumps(data), content_type='application/json')

        data["title"] = ""
        response = client.post('/labyrinth/edit/1', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert response.is_json
        assert response.get_json() == {"error": "Title is required"}

        data["title"] = "Test Labyrinth"
        data["start"] = [1, 0]
        response = client.post('/labyrinth/edit/1', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert b"Start and end coordinates are out of bounds" in response.data

        data["start"] = [1, 1]
        data["labyrinth"] = [
            [0, 1, 0, 1, 0], [0, 0, 0, 1, 0], [1, 0, 1, 1, 0], [1, 0, 1, 1, 0], [1, 0, 1, 0, 0], [1, 0, 1, 0, 0],
            [1, 0, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 0, 0],
            [1, 0, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 0, 0],
            [1, 0, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 0, 0],
            [1, 0, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 0, 0], [1, 0, 1, 0, 0],
            [1, 0, 1, 0, 0],
        ]
        response = client.post('/labyrinth/edit/1', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert b"Labyrinth dimensions must be between 5x5 and 30x50" in response.data

    def test_generate_labyrinth(self, client):
        data = {
            "dimensions": [5, 5],
            "start": [1, 1],
            "end": [5, 5]
        }

        response = client.post('/labyrinth/generate', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        result = response.get_json()
        assert len(result["matrix"]) == 5
        assert len(result["matrix"][0]) == 5
        assert bfs(matrix_to_graph(result["matrix"]), (1, 1), (5, 5)) is not None

    def test_generate_labyrinth_wrong(self, client):
        data = {
            "dimensions": [5, 51],
            "start": [1, 1],
            "end": [5, 5]
        }

        response = client.post('/labyrinth/generate', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert b"Labyrinth dimensions must be between 5x5 and 30x50" in response.data

        data["dimensions"] = [5, 5]
        data["end"] = [6, 5]
        response = client.post('/labyrinth/generate', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 400
        assert b"Start and end coordinates are out of bounds" in response.data
