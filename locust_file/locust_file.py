'''
Base class for locus tasks
'''
import json
import random

from locust import HttpLocust, TaskSet, task


class UserBehaviour(TaskSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth_token = ''
        self.headers = {
            'content-type': 'application/json',
            'Accept-Encoding': 'gzip'
        }
        self.credentials = {}
        self.ticket = {}


    def signup(self):
        name = 'test_user' + str(random.choice(range(1000000)))
        data = {
            'email': f'{name}@example.com',
            'first_name': name[:9],
            'last_name': name[9:],
            'password': 'password'
        }
        response = self.client.post('/auth/signup/', data=json.dumps(data), headers=self.headers, catch_response=True)
        if response.status_code == 200:
            self.credentials = dict(email=data['email'], password=data['password'])
            self.login()

    def login(self):
        with self.client.post('/auth/login/', data=self.credentials, headers=self.headers, catch_response=True) as response:
            token = json.loads(response.content).get('token')
            if token:
                self.auth_token = f'Bearer {token}'
                self.headers['Authorization'] = self.auth_token
            else:
                response.failure('Login failed')

    def on_start(self):
        self.signup()
        self.get_available_flights()
        self.book_flight()

    @task(4)
    def get_available_flights(self):
        with self.client.get('/flight/', headers=self.headers, catch_response=True) as response:
            if response.status_code != 200:
                response.failure('Getting flights failed')
            flights = json.loads(response.content)
            if response.status_code == 200 and flights[0].get('id'):
                self.flight_to_book = flights[random.choice(range(len(flights)))]

    @task(3)
    def get_flight_to_book(self):
        self.client.get(f'/flight/{self.flight_to_book["id"]}/', headers=self.headers)

    @task(1)
    def book_flight(self):
        if 'Authorization' not in self.headers or not self.flight_to_book.get('id'):
            return
        with self.client.post(
            '/ticket/',
            data=json.dumps({'flight': self.flight_to_book['id']}),
            headers=self.headers, catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure('Booking flight failed')
            self.ticket = json.loads(response.content)

    @task(4)
    def get_ticket(self):
        if self.ticket.get('id'):
            self.client.get(f'/ticket/{self.ticket["id"]}/', headers=self.headers)


class LocustUser(HttpLocust):
    task_set = UserBehaviour
    min_wait = 2000
    max_wait = 8000
