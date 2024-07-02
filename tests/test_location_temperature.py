import pytest
from app.main import app
from app.utils.location_temperature import get_location_and_temperature
import requests

@pytest.fixture
def mock_requests(mocker):
    mock_ipstack_response = {
        "city": "Mountain View",
        "latitude": 37.386,
        "longitude": -122.0838
    }
    mock_openweathermap_response = {
        "main": {
            "temp": 15.0
        }
    }

    mocker.patch('requests.get', side_effect=[
        mocker.Mock(status_code=200, json=lambda: mock_ipstack_response),
        mocker.Mock(status_code=200, json=lambda: mock_openweathermap_response)
    ])

@pytest.fixture
def mock_requests_error(mocker):
    mocker.patch('requests.get', side_effect=requests.exceptions.RequestException)

def test_valid_ip_returns_correct_city_and_temperature(mock_requests):
    client_ip = "8.8.8.8"

    city, temperature = get_location_and_temperature(client_ip)

    assert city == "Mountain View"
    assert temperature == 15.0

def test_invalid_ip_address_format(mock_requests_error):
    client_ip = "invalid_ip"

    city, temperature = get_location_and_temperature(client_ip)

    assert city is None
    assert temperature == "Unknown"

def test_network_issues_request_failures(mock_requests_error):
    client_ip = "8.8.8.8"

    city, temperature = get_location_and_temperature(client_ip)

    assert city is None
    assert temperature == "Unknown"
