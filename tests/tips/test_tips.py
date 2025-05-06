class TestTips:
    def test_tips_route_successful(self, client, mocker):
        with client.session_transaction() as sess:
            sess['user_id'] = 1

        mock_categories = [
            {'ID': 1, 'name': 'rent'},
            {'ID': 2, 'name': 'groceries'},
            {'ID': 3, 'name': 'spending'},
            {'ID': 4, 'name': 'paycheck'},
            {'ID': 5, 'name': 'savings'},
        ]
        mock_transactions = [
            {'category_id': 1, 'title': 'Rent', 'amount': '1000', 'expense': True, 'user_id': 1},
            {'category_id': 4, 'title': 'Paycheck', 'amount': '3000', 'expense': False, 'user_id': 1},
            {'category_id': 2, 'title': 'Groceries', 'amount': '250', 'expense': True, 'user_id': 1},
            {'category_id': 3, 'title': 'Shopping', 'amount': '300', 'expense': True, 'user_id': 1},
            {'category_id': 5, 'title': 'Savings', 'amount': '500', 'expense': False, 'user_id': 1},
        ]

        mocker.patch("db.get_categories_of_user", return_value=mock_categories)
        mocker.patch("db.get_transactions_of_user", return_value=mock_transactions)
        mocker.patch("db.get_category_name_by_id", side_effect=lambda _, cid: {
            1: "rent", 2: "groceries", 3: "spending", 4: "paycheck", 5: "savings"
        }[cid])

        expected_tips = "You're doing great!, Consider reducing your spending."
        mocker.patch("suggestions.get_budget_tips", return_value=expected_tips)

        response = client.get("/tips/")
        
        assert response.status_code == 200
        for tip in expected_tips:
            assert tip in response.get_data(as_text=True)
    def test_tips_route_no_data(self, client, mocker):
        with client.session_transaction() as sess:
            sess['user_id'] = 1
        
        mock_categories = [
            {'ID': 1, 'name': 'rent'},
            {'ID': 2, 'name': 'groceries'},
            {'ID': 3, 'name': 'spending'},
            {'ID': 4, 'name': 'paycheck'},
            {'ID': 5, 'name': 'savings'},
        ]
        mock_transactions = []
        mocker.patch("db.get_categories_of_user", return_value=mock_categories)
        mocker.patch("db.get_transactions_of_user", return_value=mock_transactions)

        response = client.get("/tips/", follow_redirects=True)
        print(response.data)
        assert b"No data entered" in response.data