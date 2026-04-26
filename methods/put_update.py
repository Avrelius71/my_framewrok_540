import requests
from methods.base_method import BaseMethod
from methods.validations.method_validations import Booking
from faker import Faker
import random


fake = Faker()


class PutUpdate(BaseMethod):
    data = None

    def put_update(self, id, data=None, token=None, validate_reqst=True, validate_resp=True):
        if data is None:
            data = {
                'firstname': fake.first_name(),
                'lastname': fake.last_name(),
                'totalprice': random.randint(0, 1000),
                'depositpaid': random.choice([True, False]),
                'bookingdates': {
                    'checkin': '2018-01-01',
                    'checkout': '2019-01-01'
                }
            }
            self.data = data
        headers = {}
        if token:
            headers = {'Cookie': f'token={token}'}
        if validate_reqst:
            Booking.model_validate(data)
        self.response = requests.put(
            f'{self.url}/booking/{id}',
            json=data,
            headers=headers
        )
        validated = None
        if validate_resp:
            validated = Booking.model_validate(self.response.json())
            return self.response, validated
        else:
            return self.response
