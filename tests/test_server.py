from server import POINTS_PER_ENTRY

class TestBooking:

    def test_not_enough_points_to_book(self, client, test_club, future_competition):
        places = int(test_club['points']) +1
        response = client.post('/purchasePlaces', data={"competition": future_competition["name"], "club": test_club['name'], "places": places})
        assert response.status_code == 200
        error_message = f"Cannot book - trying to book more than what you have."
        assert error_message in response.data.decode()

    def test_valid_booking_should_update_club_points(self, client, test_club, future_competition):  
        places = 1
        initial_club_points = int(test_club['points'])
        response = client.post('/purchasePlaces', data={"competition": future_competition["name"], "club": test_club['name'], "places": places})
        assert response.status_code == 200
        assert f'Points available: {initial_club_points-places*POINTS_PER_ENTRY}' in response.data.decode('utf-8')