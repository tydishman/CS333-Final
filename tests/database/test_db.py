import pytest
import sqlite3
import db
import os
import tempfile

class Test_db:

    @pytest.fixture
    def init_db(self, monkeypatch):
        # Create a temporary file to act as the SQLite DB. Avoids issues that I had using the in-memory database
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            temp_db_path = tmp.name

        monkeypatch.setattr(db, "DATABASE_PATH", temp_db_path)
        db.init_tables()
        yield  
        try:
            con = sqlite3.connect(temp_db_path)
            con.close()
        except Exception:
            pass
        os.remove(temp_db_path)

    def test_db_create_user_and_retrieve(self, init_db):
        db.print_schema()
        db.db_create_user("test", "test@email.com", "hashedpass")
        user = db.get_user("test")
        assert user is not None
        assert user["username"] == "test"

    def test_create_category_and_get_id(self, init_db):
        db.db_create_user("test", "test@email.com", "hashedpass")
        user = db.get_user("test")
        db.create_category(user["id"], "Fo4124od")
        retrieved_id = db.get_category_id_by_name(user["id"], "food")
        assert retrieved_id is not None

    def test_create_transaction_and_get(self, init_db):
        db.db_create_user("test", "test@email.com", "hashedpass")
        user = db.get_user("test")
        db.create_category(user["id"], "Bills")
        cat_id = db.get_category_id_by_name(user["id"], "bills")

        db.create_transaction(user["id"], "Rent", "Monthly rent", cat_id, 1000.0, True, True, "2025-04-01")
        txs = db.get_transactions_of_user(user["id"])
        assert len(txs) == 1
        assert txs[0]["title"] == "rent"

    def test_get_user_budget_and_update(self, init_db):
        db.db_create_user("test", "test@email.com", "hashedpass")
        user = db.get_user("test")
        assert db.get_user_budget(user["id"]) == 0.0

        db.save_user_budget(user["id"], 2500.0)
        assert db.get_user_budget(user["id"]) == 2500.0

    def test_create_multiple_users_and_categories(self, init_db):
        db.db_create_user("test", "test@email.com", "hashedpass")
        db.db_create_user("test2", "test2@email.com", "hashedpass")
        test_user1 = db.get_user("test")
        test_user2 = db.get_user("test2")

        db.create_category(test_user1["id"], "Fitness")
        db.create_category(test_user2["id"], "Fitness")  # Should succeed since per-user unique

        test_user1_cat = db.get_category_id_by_name(test_user1["id"], "fitness")
        test_user2_cat = db.get_category_id_by_name(test_user2["id"], "fitness")

        assert test_user1_cat != test_user2_cat