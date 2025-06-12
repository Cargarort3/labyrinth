import json
from app.auth.repositories import UserRepository


def login(client, username="example", password="password"):
    if not UserRepository.get_by_username(username):
        UserRepository.create(username, password)

    return client.post('/login', data={
        "username": username,
        "password": password
    }, follow_redirects=True)


def test_labyrinth_screens(client):
    response = client.get('/labyrinth/create')
    assert response.status_code == 200
    assert b"Introduce the labyrinth" in response.data

    login(client)
    response = client.get('/labyrinth/')
    assert response.status_code == 200
    assert b"My Labyrinths" in response.data


def test_solve_labyrinth_success(client):
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


def test_solve_labyrinth_no_solution(client):
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


def test_create_and_delete_labyrinth(client):
    login(client)

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
    login(client, "example2")
    response = client.delete('/labyrinth/1')
    assert response.status_code == 401
    assert b"You don't have permission" in response.data

    client.get('/logout')
    login(client)
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


def test_create_labyrinth_wrong(client):
    login(client)

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
