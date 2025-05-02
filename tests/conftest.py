import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.secret_key = 'testkey'
    with app.test_client() as client:
        with app.app_context():
            yield client
