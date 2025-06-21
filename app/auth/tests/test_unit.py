import pytest
from flask_login import current_user


@pytest.mark.unit
def test_auth_screens(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data

    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data


@pytest.mark.unit
def test_auth_success(client):
    response = client.post('/register', data={
        "username": "example",
        "password": "password"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data

    response = client.post('/login', data={
        "username": "example",
        "password": "password"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert current_user.is_authenticated
    assert b"Logout" in response.data

    response = client.get('/register', follow_redirects=True)
    assert response.status_code == 200
    assert b"Logout" in response.data

    response = client.get('/login', follow_redirects=True)
    assert response.status_code == 200
    assert b"Logout" in response.data

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert not current_user.is_authenticated
    assert b"Login" in response.data


@pytest.mark.unit
def test_login_wrong(client):
    client.post('/register', data={
        "username": "example",
        "password": "password"
    })

    response = client.post('/login', data={
        "username": "example",
        "password": "wrongpass"
    }, follow_redirects=True)
    assert response.status_code == 401
    assert not current_user.is_authenticated
    assert b"Login" in response.data

    response = client.post('/login', data={
        "username": "username",
        "password": "password"
    }, follow_redirects=True)
    assert response.status_code == 401
    assert not current_user.is_authenticated
    assert b"Login" in response.data


@pytest.mark.unit
def test_register_wrong(client):
    client.post('/register', data={
        "username": "example",
        "password": "password"
    })

    response = client.post('/register', data={
        "username": "example",
        "password": "password"
    }, follow_redirects=True)
    assert response.status_code == 409
    assert b"Username already taken" in response.data

    response = client.post('/register', data={
        "username": "ex",
        "password": "password"
    }, follow_redirects=True)
    assert response.status_code == 400
    assert b"Username or password doesn't meet the required length." in response.data

    response = client.post('/register', data={
        "username": "example",
        "password": "superextense password"
    }, follow_redirects=True)
    assert response.status_code == 400
    assert b"Username or password doesn't meet the required length." in response.data
