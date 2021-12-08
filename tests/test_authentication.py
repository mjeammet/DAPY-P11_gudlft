from tests.conftest import client
import server

class TestAuth:

    @staticmethod
    def load_testclubs():
        clubs = server.loadClubs('tests/test_clubs.json')

    def test_should_access_home(self, client):
        assert client.get('/').status_code == 200

    def test_should_redirect_known_email(self, client):
        clubs = self.load_testclubs()
        # email = 'test@test.fr'
        email = "john@simplylift.co"
        response = client.post('/showSummary', data={'email' : email})
        assert response.status_code == 200

    def test_unknown_email_should_return_error(self, client):
        # TODO find a way to use test clubs and competitions
        clubs = self.load_testclubs()
        email = 'certainlynotaknownadress@test.fr'
        response = client.post('/showSummary', data={'email' : email})
        assert response.status_code == 302
