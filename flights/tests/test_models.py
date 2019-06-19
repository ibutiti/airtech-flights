'''
Flight model tests
'''
from flights.models import Flight
from flights.tests.mixin import TestBase


class FlightModelTestCase(TestBase):
    '''
    Flight model test cases
    '''

    def test_persists_flight(self):
        '''Test model creates flights correctly'''
        initial_count = Flight.objects.count()

        flight = Flight.objects.create(**self.flight_data)

        with self.subTest('Test saves flight to db'):
            self.assertEqual(Flight.objects.count(), initial_count+1)

        with self.subTest('Test saves correct data'):
            for attribute, value in self.flight_data.items():
                self.assertEqual(getattr(flight, attribute), value)

        with self.subTest('Test string representation correct'):
            self.assertEqual(str(flight), f'Flight {str(flight.id)[:5]} 2019-06-20 21:00: Nairobi -> Kampala')
