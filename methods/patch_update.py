import requests
from methods.base_method import BaseMethod
from methods.validations.method_validations import PatchRequest, Booking
from faker import Faker


fake = Faker()


class PatchUpdate(BaseMethod):
    data = None

    def patch_update(self, id, data=None, token=None, validate_reqst=True, validate_resp=True):
        if data is None:
            data = {
                'firstname': fake.first_name(),
                'lastname': fake.last_name(),
            }
            self.data = data
        headers = {}
        if token:
            headers = {'Cookie': f'token={token}'}
        if validate_reqst:
            PatchRequest.model_validate(data)
        self.response = requests.patch(
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