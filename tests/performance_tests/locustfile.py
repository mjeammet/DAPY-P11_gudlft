from locust import HttpUser, task

class PerformanceTest(HttpUser):
    
    @task
    def home(self):
        self.client.get('')

    @task
    def pointsBoard(self):
        self.client.get('pointsBoard')

    @task 
    def summary(self):
        data = {"email": "kate@shelifts.co.uk"}
        self.client.post("showSummary", data=data)
    
    @task
    def booking_page(self):
        # TODO fails but I don't know why :( 
        club = "She Lifts"
        competition = "Fall Classic"
        self.client.get(f'book/{competition}/{club}', )

    @task
    def purchasePlaces(self):
        """Book test. Should not take more than 2 seconds. Default number of users: 6. """
        # TODO all tests currently failling because test dataset is not loaded and no future competition in production data
        club = "She Lifts"
        competition = "Fall Classic"
        data = {"competition": competition, "club": club, "places": 1}
        self.client.post('purchasePlaces', data=data)

    @task
    def login(self):
        response = self.client.get("logout")