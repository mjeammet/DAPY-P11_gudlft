from tests.conftest import client
import server

class TestAuth:

    @staticmethod
    def load_testclubs():
        clubs = server.loadClubs('tests/test_clubs.json')

    def test_should_access_home(self, client):
        assert client.get('/').status_code == 200

    def test_shouldnot_access_book_without_login(self, client):
        test_competition = "Test Competition"
        test_club_name = "Test Club"
        # response = client.get(f'book/${test_competition}/${test_club_name}')
        response = client.get('book/Spring Festival/She Lifts')
        assert response.status_code == 405
