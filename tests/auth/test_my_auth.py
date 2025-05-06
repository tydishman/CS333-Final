import pytest
import my_auth
from werkzeug.security import generate_password_hash

class TestMyAuth:
    def test_create_user_success(self, mocker):
        mocker.patch("db.db_create_user")
        mocker.patch("db.get_user", return_value={"id": 1})
        mocker.patch("db.create_category")

        result = my_auth.create_user("testuser", "test@email.com", "password123")
        assert result is True

    def test_create_user_failure(self, mocker):
        mocker.patch("db.db_create_user", side_effect=Exception("Fail"))

        result = my_auth.create_user("testuser", "test@email.com", "password123")
        assert result is False

    def test_init_default_categories(self, mocker):
        mock_create = mocker.patch("db.create_category")
        my_auth.init_default_categories(1, ["a", "b"])
        assert mock_create.call_count == 2


    def test_login_user_valid_credentials(self, mocker):
        hashed_pw = generate_password_hash("secret")
        mocker.patch("db.get_user", return_value={"password_hash": hashed_pw})

        assert my_auth.login_user("testuser", "secret") is True

    def test_login_user_invalid_password(self, mocker):
        hashed_pw = generate_password_hash("secret")
        mocker.patch("db.get_user", return_value={"password_hash": hashed_pw})

        assert my_auth.login_user("testuser", "wrong") is False

    def test_login_user_user_not_found(self, mocker):
        mocker.patch("db.get_user", return_value=None)

        assert my_auth.login_user("ghost", "secret") is False

    def test_login_user_from_form_success(self, mocker):
        hashed_pw = generate_password_hash("secret")
        mocker.patch("db.get_user", return_value={"id": 1, "password_hash": hashed_pw})

        user = my_auth.login_user_from_form("testuser", "secret")
        assert user is not None
        assert user["id"] == 1

    def test_login_user_from_form_failure(self, mocker):
        mocker.patch("db.get_user", return_value=None)

        user = my_auth.login_user_from_form("ghost", "wrong")
        assert user is None
