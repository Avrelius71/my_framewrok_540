"""payloads для проверки валидации ауса"""
negative_data_auth = [
    {'username': '', 'password': ''},
    {'username': 'admin', 'password': ''},
    {'username': '', 'password': 'password123'}
]

"""payloads для проверки обязательности полей при создании брони"""
negative_data_create_bok = [
    {
        'lastname': 'b',
        'totalprice': 100,
        'depositpaid': True,
        'bookingdates':
            {'checkin': '2018-01-01', 'checkout': '2019-01-01'},
        'additionalsneeds': 'b'
    },
{
        'firstname': 'a',
        'totalprice': 100,
        'depositpaid': True,
        'bookingdates':
            {'checkin': '2018-01-01', 'checkout': '2019-01-01'},
        'additionalsneeds': 'b'
    },
{
        'firstname': 'a',
        'lastname': 'b',
        'depositpaid': True,
        'bookingdates':
            {'checkin': '2018-01-01', 'checkout': '2019-01-01'},
        'additionalsneeds': 'b'
    },
{
        'firstname': 'a',
        'lastname': 'b',
        'totalprice': 100,
        'bookingdates':
            {'checkin': '2018-01-01', 'checkout': '2019-01-01'},
        'additionalsneeds': 'b'
    },
{
        'firstname': 'a',
        'lastname': 'b',
        'totalprice': 100,
        'depositpaid': True,
        'additionalsneeds': 'b'
    }
]
