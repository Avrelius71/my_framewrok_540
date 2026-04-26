from methods.base_method import BaseMethod
from methods.validations.method_validations import RequestCreateBooking, ResponseCreateBooking
import requests
import random
from faker import Faker


fake = Faker()


class CreateBooking(BaseMethod):
    data = None

    def create_booking(self, data=None, validation_reqst=True, validation_resp=True):
        if data is None:
            data = {
                'firstname': fake.first_name(),
                'lastname': fake.last_name(),
                'totalprice': random.randint(0, 1000),
                'depositpaid': random.choice([True, False]),
                'bookingdates': {
                    'checkin': '2018-01-01',
                    'checkout': '2019-01-01'
                },
                'additionalneeds': fake.text(max_nb_chars=20)
            }
            self.data = data
        if validation_reqst:
            RequestCreateBooking.model_validate(data)
        self.response = requests.post(
            f'{self.url}/booking',
            json=data
        )
        validated = None
        if validation_resp:
            validated = ResponseCreateBooking.model_validate(self.response.json())
            return self.response, validated
        else:
            return self.response

