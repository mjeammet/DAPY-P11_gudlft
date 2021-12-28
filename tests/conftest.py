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
def future_competition():
    competitions = loadCompetitions('tests/test_dataset.json')
    return competitions[1]

@pytest.fixture
def future_empty_competition():
    competitions = loadCompetitions('tests/test_dataset.json')
    return competitions[2]

@pytest.fixture
def past_competition():
    competitions = loadCompetitions('tests/test_dataset.json')
    return competitions[0]

@pytest.fixture
def zero_point_club():
    clubs = loadClubs('tests/test_dataset.json')
    return [club for club in clubs if club['points'] == 0][0]

@pytest.fixture
def hundred_point_club():
    clubs = loadClubs('tests/test_dataset.json')
    return [club for club in clubs if club['points'] == 100][0]