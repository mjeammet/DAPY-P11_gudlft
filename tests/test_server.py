from server import loadClubs

class TestPointsBoard:

    def test_should_access_home(self, client):
        assert client.get('/').status_code == 200

    def test_board_correctly_displays_clubs(self, client):
        response = client.get('/pointsBoard')
        assert response.status_code == 200

        clubs = loadClubs('tests/test_dataset.json')
        data = response.data.decode('utf-8')
        for club in clubs:
            assert club['name'] in data
            assert str(club["points"]) in data

    # TODO find a way to test that board is empty when clubs == []

