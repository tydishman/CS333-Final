import pytest
from datetime import datetime
import db_interface

class TestDBInterface:
    mock_transactions = [
        {
            "created_at": "2025-03-15",
            "amount": 100,
            "expense": True,
            "title": "Groceries",
            "description": "Weekly groceries"
        },
        {
            "created_at": "2025-03-14",
            "amount": 200,
            "expense": False,
            "title": "Salary",
            "description": "Monthly salary"
        }
    ]

    def test_find_events(self, mocker):
        mocker.patch("db_interface.db.get_transactions_of_user", return_value=TestDBInterface.mock_transactions)
        events = db_interface.find_events(user_id=1)
        assert len(events) == 2
        assert events[0]["type"] == "expense"
        assert events[1]["type"] == "income"
        assert events[0]["date"] == datetime(2025, 3, 15)

    def test_add_transaction_success(self, mocker):
        mocker.patch("db_interface.get_category_id_by_name", return_value=1)
        mock_create = mocker.patch("db_interface.db.create_transaction")
        result = db_interface.add_transaction(1, "title", "desc", "cat", 50.0, False, True, "2025-03-15")
        mock_create.assert_called_once()
        assert result is True

    def test_add_transaction_invalid_category(self, mocker):
        mocker.patch("db_interface.get_category_id_by_name", return_value=None)
        result = db_interface.add_transaction(1, "title", "desc", "invalid_cat", 50.0, False, True, "2025-03-15")
        assert result is False

    def test_add_transaction_db_exception(self, mocker):
        mocker.patch("db_interface.get_category_id_by_name", return_value=1)
        mocker.patch("db_interface.db.create_transaction", side_effect=Exception("DB error"))
        result = db_interface.add_transaction(1, "title", "desc", "cat", 50.0, False, True, "2025-03-15")
        assert result is False

    def test_add_category_success(self, mocker):
        mock_create = mocker.patch("db_interface.db.create_category")
        result = db_interface.add_category(1, "Utilities")
        mock_create.assert_called_once()
        assert result is True

    def test_add_category_failure(self, mocker):
        mocker.patch("db_interface.db.create_category", side_effect=Exception("Fail"))
        result = db_interface.add_category(1, "Utilities")
        assert result is False

    def test_get_category_id_by_name_success(self, mocker):
        mocker.patch("db_interface.db.get_category_id_by_name", return_value=3)
        result = db_interface.get_category_id_by_name(1, "Groceries")
        assert result == 3

    def test_get_category_id_by_name_exception(self, mocker):
        mocker.patch("db_interface.db.get_category_id_by_name", side_effect=Exception("DB error"))
        result = db_interface.get_category_id_by_name(1, "Invalid")
        assert result is None
