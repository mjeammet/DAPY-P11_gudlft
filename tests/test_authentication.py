from tests.conftest import client
import server

class TestAuth:

    @staticmethod
    def load_testclubs():
        clubs = server.loadClubs('tests/test_clubs.json')

    def test_should_redirect_known_email(self, client):
        clubs = self.load_testclubs()
        email = 'test@test.fr'
        # email = "john@simplylift.co"
        response = client.post('/showSummary', data={'email' : email})
        assert response.status_code == 200

    def test_should_access_home(self, client):
        assert client.get('/').status_code == 200

    def test_shouldnt_access_summary_if_unregistered(self, client):
        response = client.get('/showSummary')
        assert response.status_code == 405
    
    def test_shouldnt_access_booking_if_unregistered(self, client):
        test_competition = "Test Festival"
        response = client.get(f'/book/${test_competition}/Test Club')
        assert response.status_code == 405

