import sqlite3
import requests
import googlemaps
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize the Google Maps client with the API key
gmaps = googlemaps.Client(key='AIzaSyDuo47mcsePpGDG3h1uTbJPcR-sX7mw54I')

def get_incident_details(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT incident_number, incident_time, incident_location FROM incidents")
    incidents = cursor.fetchall()
    conn.close()
    return incidents

def fetch_weather_data_for_location(incident_details):
    incident_number, incident_time_str, location = incident_details
    try:
        # Convert incident time string to datetime object
        incident_time = datetime.strptime(incident_time_str, '%m/%d/%Y %H:%M')
        geocode_result = gmaps.geocode(location + ', Norman, OK')
        if geocode_result:
            lat_lng = geocode_result[0]['geometry']['location']
            lat, lng = lat_lng['lat'], lat_lng['lng']
            formatted_date = incident_time.strftime('%Y-%m-%d')
            # Prepare request parameters
            params = {
                'latitude': lat,
                'longitude': lng,
                'start_date': formatted_date,
                'end_date': formatted_date,
                'hourly': 'weather_code',
                'timezone': 'auto'
            }
            # Send request to Open-Meteo API
            response = requests.get("https://archive-api.open-meteo.com/v1/archive", params=params)
            if response.status_code == 200:
                data = response.json()
                if 'hourly' in data and 'weather_code' in data['hourly']:
                    weather_code_str = str(data['hourly']['weather_code'][0]).zfill(2)
                    return incident_number, weather_code_str
    except Exception as e:
        print(f"Error processing {incident_number} located at {location}: {e}")
    return incident_number, "Not Available"

def get_weather_map(db_path='resources/normanpd.db'):
    incidents = get_incident_details(db_path)
    weather_map = {}
    # Use ThreadPoolExecutor for concurrent weather data retrieval
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_incident = {executor.submit(fetch_weather_data_for_location, incident): incident for incident in incidents}
        for future in as_completed(future_to_incident):
            incident_number, weather_code = future.result()
            # Format the weather code with leading zero if it is a single digit
            weather_code_str = str(weather_code).zfill(2)
            weather_map[incident_number] = weather_code_str
    return weather_map


if __name__ == "__main__":
    weather_map = get_weather_map()
    for incident_number, weather_code in weather_map.items():
        print(f"Incident Number: {incident_number}, Weather Code: {weather_code}")
