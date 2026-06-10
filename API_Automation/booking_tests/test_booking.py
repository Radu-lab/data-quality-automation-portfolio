import requests
from payloads import create_payload, update_payload
from helpers import get_valid_booking_id,validate_booking_structure
from helpers import assert_status


def test_get_all_bookings(base_url):
    response = requests.get(f"{base_url}/booking")
    assert_status(response,200)
    bookings = response.json()
    assert len(bookings) > 0

def test_get_single_booking(base_url):
    booking_id = get_valid_booking_id(base_url)
    response = requests.get(f"{base_url}/booking/{booking_id}")
    assert_status(response,200)
    validate_booking_structure(response.json())


def test_create_booking(base_url):
    response = requests.post(f"{base_url}/booking/",json=create_payload)
    assert_status(response,200)
    booking = response.json()
    assert booking['booking']['firstname'] == "Radu"

def test_update_booking(base_url,auth_headers):
    booking_id = get_valid_booking_id(base_url)
    response = requests.put(f"{base_url}/booking/{booking_id}",json = update_payload,headers = auth_headers)
    assert_status(response,200)

def test_delete_booking(base_url, auth_headers):
    booking_id = get_valid_booking_id(base_url)
    response = requests.delete(f"{base_url}/booking/{booking_id}",headers = auth_headers)
    assert_status(response,201)
    check = requests.get(f"{base_url}/booking/{booking_id}")
    assert_status(check,401)

