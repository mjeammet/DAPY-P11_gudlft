import pytest
from server import create_app, loadClubs, loadCompetitions

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        # with app.app_context():
        #     init_db()
        yield client

@pytest.fixture
def test_club():
    return loadClubs('tests/test_dataset.json')[0]

@pytest.fixture
def test_competition():
    return loadCompetitions('tests/test_dataset.json')[0]