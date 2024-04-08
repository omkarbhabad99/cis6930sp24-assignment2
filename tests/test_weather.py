import pytest
from unittest.mock import patch
from weather import fetch_weather_data_for_location, get_weather_map

# Example test for fetch_weather_data_for_location
@patch('weather.gmaps.geocode')
@patch('weather.requests.get')
def test_fetch_weather_data_for_location_simple(mock_get, mock_geocode):
    # Setup a simple mock response for geocoding and weather API
    mock_geocode.return_value = [{'geometry': {'location': {'lat': 35.222567, 'lng': -97.439478}}}]
    mock_get.return_value.json.return_value = {
        "hourly": {
            "weather_code": [100]
        }
    }

    incident_details = ("2024-00014834", "3/1/2024 0:05", "4TH/SUNNYLANE")
    expected_weather_code = "Not Available"
    
    # Execute the function with the mocked responses
    _, weather_code = fetch_weather_data_for_location(incident_details)
    
    # Assert the expected outcome
    assert weather_code == expected_weather_code, f"Expected weather code {expected_weather_code}, but got {weather_code}"

# Example test for get_weather_map with minimal setup
@patch('weather.get_incident_details')
@patch('weather.fetch_weather_data_for_location')
def test_get_weather_map_simple(mock_fetch_weather, mock_get_incident_details):
    # Setup mock return values to directly return the expected outcome
    mock_get_incident_details.return_value = [("2024-00014834", "3/1/2024 0:05", "4TH/SUNNYLANE")]
    mock_fetch_weather.return_value = ("2024-00014834", "100")

    db_path = 'resources/normanpd.db'
    expected_map = {"2024-00014834": "100"}
    
    # Execute get_weather_map
    weather_map = get_weather_map(db_path)
    
    # Assert the expected outcome
    assert weather_map == expected_map, f"Expected weather map {expected_map}, but got {weather_map}"
