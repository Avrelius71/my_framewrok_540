import requests
from methods.validations.method_validations import Booking
from methods.base_method import BaseMethod


class GetBooking(BaseMethod):
    def get_booking(self, id, validate_resp=True):
        self.response = requests.get(f'{self.url}/booking/{id}')
        validated = None
        if validate_resp:
            validated = Booking.model_validate(self.response.json())
            return self.response, validated
        else:
            return self.response
