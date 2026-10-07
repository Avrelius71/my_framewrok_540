import requests
from methods.validations.method_validations import BookingIdsResponse
from methods.base_method import BaseMethod


class GetBookingIds(BaseMethod):
    def get_booking_ids(self, key = None, value = None, validate_resp=True):
        params = {}
        if key is not None and value is not None:
            params[key] = value
        self.response = requests.get(f'{self.url}/booking', params=params)
        validated = None
        if validate_resp:
            validated = BookingIdsResponse.model_validate(self.response.json())
            return self.response, validated
        else:
            return self.response
