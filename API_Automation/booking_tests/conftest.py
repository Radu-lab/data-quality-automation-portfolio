import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture()
def base_url():
    return BASE_URL

@pytest.fixture()
def auth_token():
    basic_auth = {
        "username": "admin",
        "password": "password123"
    }
    auth_response = requests.post(f"{BASE_URL}/auth", json=basic_auth)
    token = auth_response.json()['token']
    return token

@pytest.fixture()
def auth_headers(auth_token):
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Cookie": f"token={auth_token}"
    }