import requests
from methods.base_method import BaseMethod


class DeleteBooking(BaseMethod):
    def delete_booking(self, id, token=None):
        headers = {}
        if token:
            headers = {'Cookie': f'token={token}'}
        self.response = requests.delete(
            f'{self.url}/booking/{id}',
            headers=headers
        )
        return self.response
