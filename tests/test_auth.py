import pytest
import allure
from methods.post_auth import PostAuth
from negative_data import negative_data_auth
from faker import Faker
from utils.helper import Helper


fake = Faker()


@allure.feature('Auth')
class TestAuth:
    helper = Helper()

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title('Проверка авторизации с валидными данными')
    def test_auth(self):
        data = {'username': 'admin', 'password': 'password123'}
        with allure.step('Получение токена'):
            response, validate_data = PostAuth().post_auth(data)
            self.helper.attach_response(response)

        with allure.step('Проверка статус кода'):
            assert response.status_code == 200

        with allure.step('Проверка данных'):
            assert validate_data.token

    @pytest.mark.regression
    @allure.title('Проверка авторизации с неверными данными')
    def test_not_existent_user_auth(self):
        data = {'username': fake.user_name(), 'password': fake.password()}
        with allure.step('Получение токена'):
            response = PostAuth().post_auth(data, validate_reqst=False, validate_resp=False)

        with allure.step('Проверка статус кода'):
            assert response.status_code == 200

        with allure.step('Проверка ошибки'):
            assert response.json()['reason'] == 'Bad credentials'

    @pytest.mark.regression
    @allure.title('Проверка с невалидными данными авторизации')
    @pytest.mark.parametrize('data', negative_data_auth)
    def test_negativ_data_auth(self, data):
        with allure.step('Получение токена'):
            response = PostAuth().post_auth(data, validate_reqst=False, validate_resp=False)

        with allure.step('Проверка статус кода'):
            assert response.status_code == 200

        with allure.step('Проверка ошибки'):
            assert response.json()['reason'] == 'Bad credentials'
