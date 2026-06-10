from datetime import datetime

import requests

def get_valid_booking_id(base_url):
    bookings = requests.get(f"{base_url}/booking").json()
    return bookings[0]['bookingid']

def validate_booking_structure(booking):
    assert 'firstname' in booking
    assert 'lastname' in booking
    assert isinstance(booking['totalprice'],(int,float))
    assert isinstance(booking['depositpaid'],bool)
    assert 'checkin' in booking['bookingdates']
    assert 'checkout' in booking['bookingdates']
    try:
        datetime.strptime(booking['bookingdates']['checkin'], '%Y-%m-%d')
        validDate = True
    except ValueError:
        validDate = False
    assert validDate, 'Checkin is not a valid date'

def assert_status(response, expected):
    assert response.status_code == expected, f"Expected {expected}, got {response.status_code}"