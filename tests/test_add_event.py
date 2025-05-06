import pytest
from flask import url_for

class TestAddEvent:
    
    @pytest.fixture
    def existing_data(self):
        out = {
            "name" : "test_name",
            "description" : "test_desc",
            "amount" : "1099.99",
            "category" : "Spending",
            "newCategory" : "False",
            "type" : "expense",
            "date" : "2025-04-01"
        }
        return out
    @pytest.fixture
    def new_data(self):
        out = {
            "name" : "test_name",
            "description" : "test_desc",
            "amount" : "1099.99",
            "category" : "__new__",
            "newCategory" : "test_category",
            "type" : "expense",
            "date" : "2025-04-01"
        }
        return out
    
    def test_unauthorized_redirect(self, client):
        response = client.post("/add_event/")
        assert response.status_code == 302

        response = client.post("/add_event/", follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == url_for('landing')

    def test_add_category_fail(self, client, new_data, mocker):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        mocker.patch("db_interface.add_category", return_value=False)
        response = client.post("/add_event/", data=new_data, follow_redirects=False)
        assert response.status_code == 302

    def test_add_category(self, client, new_data, mocker):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        mocker.patch("db_interface.add_category", return_value=True)
        mocker.patch("db_interface.add_transaction", return_value=True)

        response = client.post("/add_event/", data=new_data, follow_redirects=False)
        assert response.status_code == 302

    def test_existing_category(self, client, existing_data, mocker):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        mocker.patch("db_interface.add_category", return_value=True)
        mocker.patch("db_interface.add_transaction", return_value=True)
        
        response = client.post("/add_event/", data=existing_data, follow_redirects=False)
        assert response.status_code == 302

    def test_add_transaction_fail(self, client, existing_data, mocker):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        mocker.patch("db_interface.add_category", return_value=True)
        mocker.patch("db_interface.add_transaction", return_value=False)
        
        response = client.post("/add_event/", data=existing_data, follow_redirects=False)
        assert response.status_code == 302

class TestAddRecurringEvent:
    @pytest.fixture
    def data(self):
        data = {
            "name" : "test_recurring_name",
            "description" : "test_desc",
            "amount" : "1099.99",
            "category" : "Spending",
            "newCategory" : "False",
            "type" : "expense",
            "date" : "2025-04-01",
            "recurring" : "True",
        }
        return data

    def test_add_weekly_recurring_event(self, client, data, mocker):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        data["recurrence_type"] = "weekly"

        mocker.patch("db_interface.add_category", side_effect=Exception)
        mock_db_interface_add_transaction = mocker.patch("db_interface.add_transaction")

        client.post("/add_event/", data=data)

        assert mock_db_interface_add_transaction.call_count == 6

    def test_add_biweekly_recurring_event(self, client, data, mocker):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        data["recurrence_type"] = "biweekly"

        mocker.patch("db_interface.add_category", side_effect=Exception)
        mock_db_interface_add_transaction = mocker.patch("db_interface.add_transaction")

        client.post("/add_event/", data=data)

        assert mock_db_interface_add_transaction.call_count == 6

    def test_add_monthly_recurring_event(self, client, data, mocker):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        data["recurrence_type"] = "monthly"

        mocker.patch("db_interface.add_category", side_effect=Exception)
        mock_db_interface_add_transaction = mocker.patch("db_interface.add_transaction")

        client.post("/add_event/", data=data)

        assert mock_db_interface_add_transaction.call_count == 6

    def test_add_custom_recurring_event(self, client, data, mocker):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        data["recurrence_type"] = "custom_days"
        data["custom_days"] = "3,4, 5"

        mocker.patch("db_interface.add_category", side_effect=Exception)
        mock_db_interface_add_transaction = mocker.patch("db_interface.add_transaction")

        client.post("/add_event/", data=data)

        # call count increases: f(x) = 15x + 1
        assert mock_db_interface_add_transaction.call_count == 46
    
