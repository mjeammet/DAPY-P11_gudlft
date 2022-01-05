class TestIntegrationClass:

    def test_should_login_book_and_logout(self, client, test_club, future_competition):
        """Tests login in and booking an entry for a future competition."""
        assert client.get('/').status_code == 200

        # Login
        data = {'email' : test_club["email"]}
        response = client.post('/showSummary', data=data)
        assert response.status_code == 200

        # Reach booking page
        booking_page = client.get(f'/book/{future_competition["name"]}/{test_club["name"]}')
        assert booking_page.status_code == 200

        # Actually book one entry
        places = 1
        initial_club_points = test_club['points']
        initial_competition_places = int(future_competition["numberOfPlaces"])
        data = {"club": test_club["name"], "competition": future_competition["name"], "places": places}
        reservation = client.post('/purchasePlaces', data=data)
        assert reservation.status_code == 200
        remaining_points = f'Points available: {initial_club_points-places}'
        remaining_places = f"Number of Places: {initial_competition_places-places}"
        assert remaining_points in reservation.data.decode('utf-8')        
        # assert remaining_places in response.data.decode('utf-8')

        logout_page = client.get("/logout")
        assert logout_page.status_code == 302