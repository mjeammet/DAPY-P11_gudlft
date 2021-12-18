class TestAuth:

    def test_valid_booking_should_display_confirmation_message(self, client, test_club, test_competition):
        places = 1
        initial_club_points = int(test_club['points'])
        remainingPlaces = int(test_competition['numberOfPlaces'])
        response = client.post('/purchasePlaces', data={"competition": test_competition["name"], "club": test_club['name'], "places": places})
        assert response.status_code == 200
        confirmation_message = "Great-booking complete!"
        assert confirmation_message in response.data.decode('utf-8')
        assert f'Points available: {initial_club_points-places}' in response.data.decode('utf-8')
        # assert test_competition['numberOfPlaces'] == remainingPlaces-places

    def test_not_enough_points_to_book(self, client, test_club, test_competition):
        places = int(test_club['points']) +1
        response = client.post('/purchasePlaces', data={"competition": test_competition["name"], "club": test_club['name'], "places": places})
        assert response.status_code == 200
        error_message = f"Cannot book - trying to book more than what you have."
        assert error_message in response.data.decode()

    def test_shouldnt_book_more_than_remaining(self, client, test_club, test_competition):
        places = int(test_competition['numberOfPlaces']) +1
        response = client.post('/purchasePlaces', data={"competition": test_competition["name"], "club": test_club['name'], "places": places})
        assert response.status_code == 200
        error_message = "Cannot book - trying to book more than what remains."
        assert error_message in response.data.decode()

    def test_shouldnt_book_when_0_points(self, client, zero_point_club):
        response = client.post('/showSummary', data={"email": zero_point_club["email"]})
        assert b'cannot make any reservation!' in response.data
        assert b'Book places' not in response.data