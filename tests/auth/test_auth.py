from flask import url_for

class TestSignup:
    def test_signup_success(self, client, mocker):
        mock_create_user = mocker.patch("my_auth.create_user", return_value=True)

        response = client.post("/signup/", data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }, follow_redirects=True)

        assert b"Sign up successful" in response.data
        mock_create_user.assert_called_once_with("testuser", "test@example.com", "password123")

    def test_signup_existing_email(self, client, mocker):
        mock_create_user = mocker.patch("my_auth.create_user", return_value=False)

        response = client.post("/signup/", data={
            "username": "existinguser",
            "email": "existing@example.com",
            "password": "password123"
        }, follow_redirects=True)

        assert b"Sign up failed. Please try again" in response.data
        mock_create_user.assert_called_once_with("existinguser", "existing@example.com", "password123")

    def test_signup_missing_password(self, client):
        response = client.post("/signup/", data={
            "username": "existinguser",
            "email": "existing@example.com",
            "password": ""
        }, follow_redirects=True)

        assert b"Please fill out all fields." in response.data
    
    def test_signup_missing_email(self, client):
        response = client.post("/signup/", data={
            "username": "existinguser",
            "email": "",
            "password": "password123"
        }, follow_redirects=True)

        assert b"Please fill out all fields." in response.data

    def test_signup_missing_username(self, client):
        response = client.post("/signup/", data={
            "username": "",
            "email": "existing@example.com",
            "password": "password123"
        }, follow_redirects=True)

        assert b"Please fill out all fields." in response.data

class TestLogin:
    def test_login_username_successful(self, client, mocker):
        mock_user = {
            'id' : 1,
            'username' : 'testuser',
            'email' : 'test@example.com'
        }
        
        mocker.patch("my_auth.login_user_from_form", return_value=mock_user)
        response = client.post("/login/", data={
            "username": "testuser",
            "email": "",
            "password": "password123"
        }, follow_redirects=True)

        # should be redirected
        assert response.status_code == 200
        assert response.request.path == url_for('personalView')

        with client.session_transaction() as se:
            assert se['user_id'] == mock_user['id']
            assert se['username'] == mock_user['username']

    def test_login_email_successful(self, client, mocker):
        mock_user = {
            'id' : 1,
            'username' : 'testuser',
            'email' : 'test@example.com'
        }
        
        mocker.patch("my_auth.login_user_from_form", return_value=mock_user)
        response = client.post("/login/", data={
            "username": "",
            "email": "test@example.com",
            "password": "password123"
        }, follow_redirects=True)

        # should be redirected
        assert response.status_code == 200
        assert response.request.path == url_for('personalView')

        with client.session_transaction() as se:
            assert se['user_id'] == mock_user['id']
            assert se['username'] == mock_user['username']

    def test_login_fail(self, client, mocker):
        mock_login_user = mocker.patch("my_auth.login_user_from_form", return_value=None)

        response = client.post("/login/", data={
            "username": "invaliduser",
            "email": "",
            "password": "badpass"
        }, follow_redirects=True)

        assert b"Invalid username or password" in response.data
        mock_login_user.assert_called_once_with("invaliduser", "badpass")
