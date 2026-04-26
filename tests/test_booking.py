import allure
import pytest
from negative_data import negative_data_create_bok
from faker import Faker
from methods.delete_booking import DeleteBooking
import random
from utils.helper import Helper


fake = Faker()


@pytest.fixture
def created_booking_ids():
    """Список ID созданных броней для cleanup."""
    return []


@pytest.fixture
def cleanup_booking(created_booking_ids, set_token):
    """Фикстура для удаления тестовых пользователей после теста."""
    yield  # Тест выполняется здесь

    # Cleanup после теста
    for booking_id in created_booking_ids:
        try:
            DeleteBooking().delete_booking(booking_id, set_token)
        except Exception as e:
            print(f"Ошибка при удалении {booking_id}: {e}")


@allure.feature('Booking')
class TestBooking:
    helper = Helper()

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title('Проверка создания брони со всеми параметрами')
    def test_create_booking_all_params(self, booking_create, created_booking_ids, cleanup_booking):
        with allure.step('Создание брони'):
            response, validate_data = booking_create.create_booking()
            self.helper.attach_response(response)

        with allure.step('Проверка статус кода'):
            assert response.status_code == 200

        with allure.step('Проверка полученных данных'):
            assert validate_data.booking.firstname == booking_create.data['firstname']
            assert validate_data.booking.totalprice == booking_create.data['totalprice']

        created_booking_ids.append(validate_data.bookingid)

    @pytest.mark.regression
    @allure.title('Проверка создания брони с обязательными параметрами')
    def test_create_booking_required_params(self, booking_create, created_booking_ids, cleanup_booking):
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
        with allure.step('Создание брони'):
            response, validate_data = booking_create.create_booking(data)
            self.helper.attach_response(response)

        with allure.step('Проверка статус кода'):
            assert response.status_code == 200

        with allure.step('Проверка полученных данных'):
            assert validate_data.booking.firstname == data['firstname']
            assert validate_data.booking.totalprice == data['totalprice']

        created_booking_ids.append(validate_data.bookingid)

    @pytest.mark.regression
    @allure.title('Проверка создания брони с невалидными данными')
    @pytest.mark.parametrize('data', negative_data_create_bok)
    def test_negative_create_booking(self, booking_create, data):
        with allure.step('Cоздание брони'):
            response = booking_create.create_booking(data, validation_reqst=False, validation_resp=False)

        with allure.step('Проверка статус кода'):
            assert response.status_code == 500
            assert response.text == 'Internal Server Error'

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title('Проверка получения брони по id')
    def test_get_book(self, get_book, create_booking):
        id = create_booking['bookingid']
        request_data = create_booking['request_data']
        with allure.step('Получение брони по ID'):
            response, validate_data = get_book.get_booking(id)
            self.helper.attach_response(response)

        with allure.step('Проверка статус кода'):
            assert response.status_code == 200

        with allure.step('Проверка полученных данных'):
            assert validate_data.firstname == request_data['firstname']
            assert validate_data.lastname == request_data['lastname']

    @pytest.mark.regression
    @allure.title('Проверка получения брони с несуществующим id')
    def test_negative_get_book(self, get_book):
        with allure.step('Получение брони по ID'):
            response = get_book.get_booking(7777, validate_resp=False)

        with allure.step('Проверка статус кода'):
            assert response.status_code == 404
            assert response.text == 'Not Found'

    @pytest.mark.regression
    @allure.title('Проверка получения всех бронирований')
    def test_get_all_booking_ids(self, booking_ids):
        with allure.step('Получение списка бронирования'):
            response, validate_data = booking_ids.get_booking_ids()
            self.helper.attach_response(response)

        with allure.step('Проверка статус кода'):
            assert response.status_code == 200

        with allure.step('Проверка полученных данных'):
            assert len(validate_data.root) >= 0

    @pytest.mark.regression
    @allure.title('Проверка получения бронирований по фильтру')
    @pytest.mark.parametrize('key', ['lastname', 'firstname', 'checkin', 'checkout'])
    def test_get_booking_ids(self, create_booking_and_filters, booking_ids, key):
        with allure.step(f'Получение списка бронирования по {key}'):
            value = create_booking_and_filters[key]
            response, validate_data = booking_ids.get_booking_ids(key, value)
            self.helper.attach_response(response)

        with allure.step('Проверка статус кода'):
            response.status_code == 200

        with allure.step('Проверка полученных данных'):
            assert len(validate_data.root) >= 0

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title('Проверка полного обновления брони авторизованным пользователем')
    def test_put_update_authoriz(self, update_put, create_booking,
                                 set_token, get_book, created_booking_ids, cleanup_booking):
        id = create_booking['bookingid']

        with allure.step('редактирование брони'):
            response, validate_data = update_put.put_update(id=id, token=set_token)
            self.helper.attach_response(response)

        with allure.step('Проверка статус кода'):
            assert response.status_code == 200

        with allure.step('Проверка полученных данных'):
            validate_data.firstname = update_put.data['firstname']
            validate_data.lastname = update_put.data['lastname']

        with allure.step('Получение данных по id брони'):
            response2 = get_book.get_booking(id, validate_resp=False)

        with allure.step('Проверка изменения данных'):
            assert response2.json()['firstname'] == update_put.data['firstname']

        created_booking_ids.append(id)

    @pytest.mark.regression
    @allure.title('Проверка обновления брони не авторизованным пользователем')
    def test_put_update_not_authoriz(self, update_put, create_booking, get_book,
                                     created_booking_ids, cleanup_booking):
        id = create_booking['bookingid']

        with allure.step('редактирование брони'):
            response = update_put.put_update(id, validate_resp=False)

        with allure.step('Проверка статус кода'):
            assert response.status_code == 403

        with allure.step('Получение данных по id брони'):
            response2 = get_book.get_booking(id, validate_resp=False)

        with allure.step('Проверяем что данные не изменились'):
            assert response2.json()['firstname'] != update_put.data['firstname']

        created_booking_ids.append(id)

    @pytest.mark.regression
    @allure.title('Проверка обновления брони с невалидным токеном')
    def test_put_update_indalid_token(self, update_put, create_booking, get_book,
                                      created_booking_ids, cleanup_booking):
        token = '12345'
        id = create_booking['bookingid']

        with allure.step('редактирование брони'):
            response = update_put.put_update(id=id, token=token, validate_resp=False)

        with allure.step('Проверка статус кода'):
            assert response.status_code == 403

        with allure.step('Получение данных по id брони'):
            response2 = get_book.get_booking(id, validate_resp=False)

        with allure.step('Проверяем что данные не изменились'):
            assert response2.json()['firstname'] != update_put.data['firstname']

        created_booking_ids.append(id)

    @pytest.mark.regression
    @allure.title('Проверка обновления несуществующей брони')
    def test_put_update_not_found_bok(self, update_put, set_token, get_book):
        id = 77777

        with allure.step('редактирование брони'):
            response = update_put.put_update(id=id, token=set_token, validate_resp=False)

        with allure.step('Проверка статус кода'):
            response.status_code == 405

    @pytest.mark.regression
    @allure.title('Проверка частичного обновления брони авторизованным пользователем')
    def test_patch_update_authoriz(self, update_patch, create_booking, set_token, get_book,
                                   created_booking_ids, cleanup_booking):
        id = create_booking['bookingid']

        with allure.step('редактирование брони'):
            response, validate_data = update_patch.patch_update(id=id, token=set_token)
            self.helper.attach_response(response)

        with allure.step('Проверка статус кода'):
            assert response.status_code == 200

        with allure.step('Проверка полученных данных'):
            validate_data.firstname = update_patch.data['firstname']
            validate_data.lastname = update_patch.data['lastname']

        with allure.step('Получение данных по id брони'):
            response2 = get_book.get_booking(id, validate_resp=False)

        with allure.step('Проверка изменения данных'):
            assert response2.json()['firstname'] == update_patch.data['firstname']

        created_booking_ids.append(id)

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.title('Проверка удаления брони')
    def test_delete_booking(self, create_booking, delete_bok, set_token, get_book):
        id = create_booking['bookingid']
        with allure.step('Удаление брони'):
            response = delete_bok.delete_booking(id, set_token)

        with allure.step('Проверка статус кода'):
            assert response.status_code == 201

        with allure.step('Получение данных по удаленной брони'):
            response2 = get_book.get_booking(id, validate_resp=False)

        with allure.step('Проверка статус кода'):
            assert response2.status_code == 404

    @pytest.mark.regression
    @allure.title('Проверка удаления брони не авторизованным пользователем')
    def test_delete_booking_not_autoriz(self, create_booking, delete_bok,
                                        created_booking_ids, cleanup_booking, get_book):
        id = create_booking['bookingid']
        with allure.step('Удаление брони'):
            response = delete_bok.delete_booking(id)

        with allure.step('Проверка статус кода'):
            assert response.status_code == 403

        with allure.step('Проверка получения брони'):
            response2 = get_book.get_booking(id, validate_resp=False)

        with allure.step('Проверка данных'):
            assert 'firstname' in response2.json()

        created_booking_ids.append(id)

    @pytest.mark.regression
    @allure.title('Проверка удаления брони c невалидным токеном')
    def test_delete_booking_invalid_token(self, create_booking, delete_bok,
                                        created_booking_ids, cleanup_booking, get_book):
        id = create_booking['bookingid']
        token = '12345'
        with allure.step('Удаление брони'):
            response = delete_bok.delete_booking(id=id, token=token)

        with allure.step('Проверка статус кода'):
            assert response.status_code == 403

        with allure.step('Проверка получения брони'):
            response2 = get_book.get_booking(id, validate_resp=False)

        with allure.step('Проверка данных'):
            assert 'firstname' in response2.json()

        created_booking_ids.append(id)

    @pytest.mark.regression
    @allure.title('Проверка удаления несуществующей брони')
    def test_delete_booking_not_found(self, delete_bok, set_token):
        id = 7777
        with allure.step('Удаление брони'):
            response = delete_bok.delete_booking(id, set_token)

        with allure.step('Проверка статус кода'):
            assert response.status_code == 405
