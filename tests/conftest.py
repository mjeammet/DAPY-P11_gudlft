import pytest

from server import create_app, loadClubs


def init_db():
    clubs = loadClubs('tests/test_clubs.json')

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client