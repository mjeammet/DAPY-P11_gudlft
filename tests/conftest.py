import pytest
from server import create_app, loadClubs, loadCompetitions

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client
