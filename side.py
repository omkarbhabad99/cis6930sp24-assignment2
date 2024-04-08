import sqlite3
import googlemaps
import math
from concurrent.futures import ThreadPoolExecutor, as_completed

# Initialize the Google Maps client with your API key
gmaps = googlemaps.Client(key='AIzaSyDuo47mcsePpGDG3h1uTbJPcR-sX7mw54I')

def get_incident_locations(db_path):
    
    # Fetches incident locations from the 'normanpd.db' database.
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT incident_number, incident_location FROM incidents")
    locations = cursor.fetchall()
    conn.close()
    return locations

def geocode_location(location):
    
    # Function to geocode a single location using Google Maps API.
   
    try:
        result = gmaps.geocode(location + ', Norman, OK')
        if result:
            lat_lng = result[0]['geometry']['location']
            lat, lng = lat_lng['lat'], lat_lng['lng']
            return location, get_side_of_town(lat, lng)
    except Exception as e:
        pass
    return location, "Unknown"

def get_side_of_town(lat, lng):
    
    # Determines the side of town based on latitude and longitude.
    
    center_lat, center_lng = 35.220833, -97.443611
    delta_lng = lng - center_lng
    delta_lat = lat - center_lat
    angle = math.atan2(delta_lng, delta_lat)
    degree = math.degrees(angle) % 360
    
    if 22.5 < degree <= 67.5:
        return 'NE'
    elif 67.5 < degree <= 112.5:
        return 'E'
    elif 112.5 < degree <= 157.5:
        return 'SE'
    elif 157.5 < degree <= 202.5:
        return 'S'
    elif 202.5 < degree <= 247.5:
        return 'SW'
    elif 247.5 < degree <= 292.5:
        return 'W'
    elif 292.5 < degree <= 337.5:
        return 'NW'
    else:
        return 'N'

def geocode_locations_and_determine_sides(locations):
    
    # Geocodes addresses and determines the side of town for each location using multithreading.
    
    side_of_town_map = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
        
        future_to_location = {executor.submit(geocode_location, loc[1]): loc for loc in locations}
        
        # Collect results as they complete
        for future in as_completed(future_to_location):
            location, side_of_town = future.result()
            side_of_town_map[location] = side_of_town
    return side_of_town_map

def get_side_of_town_map(db_path='resources/normanpd.db'):
    
    # Fetch incident locations from the database and determine their side of town.
    
    incident_locations = get_incident_locations(db_path)
    return geocode_locations_and_determine_sides(incident_locations)

if __name__ == "__main__":
    # Example usage
    side_of_town_map = get_side_of_town_map()
    for location, side in side_of_town_map.items():
        print(f"{location}: {side}")
