import requests
from methods.base_method import BaseMethod


class TestPingRequest(BaseMethod):
    def test_ping(self):
        response = requests.get(f'{self.url}/ping')
        assert response.status_code == 201