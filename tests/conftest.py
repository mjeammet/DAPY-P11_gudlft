import pytest
from server import create_app, loadClubs, loadCompetitions

<<<<<<< HEAD
def init_db():
    clubs = loadClubs('tests/test_clubs.json')

=======
>>>>>>> origin/bug/issue#2
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
<<<<<<< HEAD
    return loadCompetitions('tests/test_dataset.json')[0]
=======
    return loadCompetitions('tests/test_dataset.json')[0]
>>>>>>> origin/bug/issue#2
