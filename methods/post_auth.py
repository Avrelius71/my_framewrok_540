import requests
from methods.base_method import BaseMethod
from methods.validations.method_validations import RequestPostAuth, ResponsePostAuth


class PostAuth(BaseMethod):
    def post_auth(self, data, validate_reqst=True, validate_resp=True):
        if validate_reqst:
            request = RequestPostAuth.model_validate(data)
        self.response = requests.post(
            f'{self.url}/auth',
            json=data
        )
        validate=None
        if validate_resp:
            validate = ResponsePostAuth.model_validate(self.response.json())
            return self.response, validate
        else:
            return self.response
