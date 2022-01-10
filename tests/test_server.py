class TestAuth:
    
    def test_valid_booking_should_update_club_points(self, client, test_club, test_competition):
        places = 1
        initial_club_points = int(test_club['points'])
        response = client.post('/purchasePlaces', data={"competition": test_competition["name"], "club": test_club['name'], "places": places})
        assert response.status_code == 200
        assert f'Points available: {initial_club_points-places}' in response.data.decode('utf-8')

    def test_valid_book_should_confirm_booked_entries(self, client, test_club, test_competition):
        places = 1
        initial_club_points = int(test_club['points'])
        response = client.post('/purchasePlaces', data={"competition": test_competition["name"], "club": test_club['name'], "places": places})
        assert response.status_code == 200
        assert f"Great, succesfully booked {places} place(s)" in response.data.decode("utf-8")