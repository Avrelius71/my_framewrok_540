import pytest
from methods.create_booking import CreateBooking
from methods.get_booking_ids import GetBookingIds
from methods.get_boking import GetBooking
from methods.post_auth import PostAuth
from methods.put_update import PutUpdate
from methods.patch_update import PatchUpdate
from methods.delete_booking import DeleteBooking


@pytest.fixture()
def booking_create():
    return CreateBooking()


@pytest.fixture()
def get_book():
    return GetBooking()


@pytest.fixture()
def booking_ids():
    return GetBookingIds()


@pytest.fixture()
def update_put():
    return PutUpdate()


@pytest.fixture()
def update_patch():
    return PatchUpdate()


@pytest.fixture()
def delete_bok():
    return DeleteBooking()


@pytest.fixture()
def create_booking():
    data = {
        'firstname': 'goga',
        'lastname': 'gaga',
        'totalprice': '777',
        'depositpaid': True,
        'bookingdates': {
            'checkin': '2018-01-01',
            'checkout': '2019-01-01'
        }
    }
    response = CreateBooking().create_booking(data, validation_reqst=False, validation_resp=False)
    yield {'bookingid': response.json()['bookingid'], 'request_data': data}


@pytest.fixture()
def create_booking_and_filters():
    data = {
        'firstname': 'goga',
        'lastname': 'gaga',
        'totalprice': '777',
        'depositpaid': True,
        'bookingdates': {
            'checkin': '2018-01-01',
            'checkout': '2019-01-01'
        }
    }
    response = CreateBooking().create_booking(data, validation_reqst=False, validation_resp=False)
    yield {
        'firstname': response.json()['booking']['firstname'],
        'lastname': response.json()['booking']['lastname'],
        'checkin': response.json()['booking']['bookingdates']['checkin'],
        'checkout': response.json()['booking']['bookingdates']['checkout']
    }


@pytest.fixture()
def set_token():
    data = {'username': 'admin', 'password': 'password123'}
    response = PostAuth().post_auth(data, validate_resp=False, validate_reqst=False)
    token = response.json()['token']
    yield token
