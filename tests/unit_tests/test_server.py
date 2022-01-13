import pytest
from datetime import datetime
from server import MAX_PER_CLUB, POINTS_PER_ENTRY, loadClubs, loadCompetitions
from tests.conftest import future_competition, test_club


class TestDatabase:

    def test_loadClubs(self):
        
        clubs = loadClubs('tests/test_dataset.json')
        expected = [{
            "name":"Test Club",
            "email":"test@test.fr",
            "points":11
            },
            {
                "name":"Zero point Club",
                "email":"zero@mail.fr",
                "points":0
            },
            {
                "name":"Hundred points Club",
                "email":"hundred@mail.fr",
                "points":100
            }]
        assert clubs == expected

    def test_loadCompetitions(self):
        
        compets = loadCompetitions('tests/test_dataset.json')
        expected = [
            {
                "date": datetime(2020, 3, 27, 10, 00, 00),
                'is_past': True,
                "name": "Past Competition",
                "numberOfPlaces": '8'
            },
            {
                "name": "Future Competition",
                "date": datetime(2030, 3, 27, 10, 00, 00),
                'is_past': False,
                "numberOfPlaces": '8'
            },
            {
                "name": "Future Empty Competition",
                "date": datetime(2030, 3, 27, 10, 00, 00),
                'is_past': False,
                "numberOfPlaces": '100'
            }]
        assert compets == expected

class TestAuth:
    
    @pytest.mark.parametrize(
        "endpoint, expected_code", [
            ('/', 200),
            ('/showSummary', 405),
            ('/purchasePlaces', 405),
            ('/logout', 302), 
            ('/pointsBoard', 200)])
            # TODO add /book/ endpoint with test club and competition (currently test dataset not loaded during parametrize)
    def test_endpoint_accesses(self, client, endpoint, expected_code):
        assert client.get(endpoint).status_code == expected_code

    def test_should_redirect_known_email(self, client, test_club):
        email = test_club["email"]
        response = client.post('/showSummary', data={'email' : email})
        assert response.status_code == 200
        assert f'Welcome, {email}' in response.data.decode()
        assert f'Points available: {test_club["points"]}' in response.data.decode()

    def test_unknown_email_should_return_error(self, client):
        email = 'certainlynotaknownadress@mail.fr'
        response = client.post('/showSummary', data={'email' : email})
        assert response.status_code == 302
        response_redirected = client.post('/showSummary', data={'email' : email}, follow_redirects = True)
        assert "Sorry, that email wasn&#39;t" in response_redirected.data.decode()


class TestBooking:

    def test_valid_book_should_confirm_booked_entries(self, client, test_club, future_competition):
        places = 1
        response = client.post('/purchasePlaces', data={"competition": future_competition["name"], "club": test_club['name'], "places": places})
        assert response.status_code == 200
        assert f"Great, succesfully booked {places} place(s)" in response.data.decode("utf-8")

    def test_valid_booking_should_update_club_points(self, client, test_club, future_competition):  
        places = 1
        initial_club_points = int(test_club['points'])
        data = {"competition": future_competition["name"], "club": test_club['name'], "places": places}
        response = client.post('/purchasePlaces', data=data)
        assert response.status_code == 200
        assert f'Points available: {initial_club_points-places*POINTS_PER_ENTRY}' in response.data.decode('utf-8')

    def test_shouldnt_book_past_competitions(self, client, test_club, past_competition):
        places = 1
        response = client.post('/purchasePlaces', data={"competition": past_competition["name"], "club": test_club['name'], "places": places})
        assert response.status_code == 400
        assert b'Cannot book past competitions.' in response.data 

    def test_not_enough_points_to_book(self, client, test_club, future_competition):
        places = int(test_club['points']) +1
        response = client.post('/purchasePlaces', data={"competition": future_competition["name"], "club": test_club['name'], "places": places})
        assert response.status_code == 200
        error_message = f"Cannot book - trying to book more than what you have."
        assert error_message in response.data.decode()

    def test_shouldnt_book_more_than_remaining(self, client, hundred_point_club, future_competition):
        places = int(future_competition['numberOfPlaces']) +1
        response = client.post('/purchasePlaces', data={"competition": future_competition["name"], "club": hundred_point_club['name'], "places": places})
        assert response.status_code == 200
        error_message = "Cannot book - trying to book more than what remains."
        assert error_message in response.data.decode()

    def test_shouldnt_book_more_than_max_per_club(self, client, hundred_point_club, future_empty_competition):
        places = MAX_PER_CLUB+1
        response = client.post('/purchasePlaces', data={"competition": future_empty_competition["name"], "club": hundred_point_club['name'], "places": places})
        assert response.status_code == 200
        error_message = f'Cannot book - Trying to book more than maximum allowed'
        assert error_message in response.data.decode('utf-8')

    def test_shouldnt_book_when_0_points(self, client, zero_point_club):
        response = client.post('/showSummary', data={"email": zero_point_club["email"]})
        assert b'cannot make any reservation!' in response.data
        assert b'Book places' not in response.data
    
    def test_not_enough_points_to_book(self, client, test_club, future_competition):
        places = int(test_club['points']) +1
        response = client.post('/purchasePlaces', data={"competition": future_competition["name"], "club": test_club['name'], "places": places})
        assert response.status_code == 200
        error_message = f"Cannot book - trying to book more than what you have."
        assert error_message in response.data.decode()


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