import pytest
from flask_login import current_user


@pytest.mark.unit
class TestAuth():
    def test_auth_screens(self, client):
        response = client.get('/register')
        assert response.status_code == 200
        assert b"Register" in response.data

        response = client.get('/login')
        assert response.status_code == 200
        assert b"Login" in response.data

    def test_auth_success(self, client):
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

        response = client.get('/profile')
        assert response.status_code == 200
        assert b"My profile" in response.data

        response = client.get('/profile/1')
        assert response.status_code == 200
        assert b"My profile" in response.data

        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert not current_user.is_authenticated
        assert b"Login" in response.data

        response = client.get('/profile/1')
        assert response.status_code == 200
        assert b"example's profile" in response.data

    def test_login_wrong(self, client):
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

    def test_register_wrong(self, client):
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

    def test_profile_not_found(self, client):
        response = client.get('/profile/1')
        assert response.status_code == 404
        assert b"User not found" in response.data
