from datetime import datetime as dt

class TestAuth:
    
    def test_should_access_home(self, client):
        assert client.get('/').status_code == 200

    def test_should_redirect_known_email(self, client, test_club):
        email = test_club["email"]
        # email = "john@simplylift.co"
        response = client.post('/showSummary', data={'email' : email})
        assert response.status_code == 200

    def test_unknown_email_should_return_error(self, client):
        email = 'certainlynotaknownadress@test.fr'
        response = client.post('/showSummary', data={'email' : email})
        assert response.status_code == 302


class TestBooking:

    def test_valid_booking_should_display_confirmation_message(self, client, test_club, future_competition):
        places = 1
        response = client.post('/purchasePlaces', data={"competition": future_competition["name"], "club": test_club['name'], "places": places})
        assert response.status_code == 200
        assert b"Great-booking complete!" in response.data

    def test_valid_booking_should_update_club_points(self, client, test_club, future_competition):
        places = 1
        initial_club_points = int(test_club['points'])
        response = client.post('/purchasePlaces', data={"competition": future_competition["name"], "club": test_club['name'], "places": places})
        assert response.status_code == 200
        assert f'Points available: {initial_club_points-places}' in response.data.decode('utf-8')

    def test_shouldnt_book_past_competitions(self, client, test_club, past_competition):
        places = 1
        response = client.post('/purchasePlaces', data={"competition": past_competition["name"], "club": test_club['name'], "places": places})
        assert response.status_code == 400
        assert b'Cannot book past competitions.' in response.data 

    def test_shouldnt_access_booking_page_past_competitions(self, client, test_club, past_competition):
        response = client.get(f'/book/{past_competition["name"]}/{test_club["name"]}')
        assert response.status_code == 400
        assert b'Cannot book past competitions.' in response.data


