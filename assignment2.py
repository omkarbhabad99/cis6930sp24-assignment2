import argparse  # Used for parsing command line arguments
import urllib.request  # For issuing HTTP requests to download PDF files
import os  
import sqlite3  # For database operations
import fitz  # PyMuPDF, used for interacting with PDF files
import ssl  # Import the SSL module for handling HTTPS requests
import tempfile  
import csv
from datetime import datetime # For working with date and time
from collections import Counter # A container that keeps count of hashable objects
import math
from side import get_side_of_town_map
from weather import get_weather_map
from ems import get_emsstat_map 
from concurrent.futures import ThreadPoolExecutor, as_completed # For running asynchronous tasks



def fetchincidents(url):
    """
    Download the PDF from the given URL and save it to a temporary file.
    
    """
    context = ssl._create_unverified_context()  # Create a context that does not verify SSL certificates
    response = urllib.request.urlopen(url, context=context) 
    
    temp_dir = tempfile.gettempdir()  # Get the path to the system's temporary directory
    file_name = os.path.join(temp_dir, 'incident.pdf') 
    
    with open(file_name, 'wb') as file: 
        file.write(response.read())  # Write the downloaded PDF content to the file
    return file_name 


def extractincidents(pdf_path):
    columns = [52.560001373291016, 150.86000061035156, 229.82000732421875, 423.19000244140625,
               623.8599853515625]

    pages = fitz.open(pdf_path)
    final_response = []
    my_dict = {}
    prev = 0
    for page in pages:
        array = page.get_text('words')
        for tuple_data in array:
            block_no = tuple_data[5]
            if block_no in my_dict:
                list_incidents = my_dict.get(block_no)
                list_incidents.append(tuple_data)
            else:
                if my_dict:
                    list_words = my_dict[prev]
                    rows = ["", "", "", "", ""]
                    for data in list_words:
                        x_coordinate = data[0]
                        text = data[4]
                        if x_coordinate == columns[0] or x_coordinate < columns[1]:
                            rows[0] = rows[0] + " " + text if rows[0] else text
                        elif x_coordinate == columns[1] or x_coordinate < columns[2]:
                            rows[1] = rows[1] + " " + text if rows[1] else text
                        elif x_coordinate == columns[2] or x_coordinate < columns[3]:
                            rows[2] = rows[2] + " " + text if rows[2] else text
                        elif x_coordinate == columns[3] or x_coordinate < columns[4]:
                            rows[3] = rows[3] + " " + text if rows[3] else text
                        else:
                            rows[4] = rows[4] + " " + text if rows[4] else text
                    if rows[2].find("NORMAN POLICE DEPARTMENT") == -1 and rows[2].find(
                            "Daily Incident Summary") == -1 and rows[1].find("Incident Number") == -1:
                        final_response.append(tuple(rows))
                    rows = ["", "", "", "", ""]
                    my_dict.clear()
                list = []
                list.append(tuple_data)
                my_dict[block_no] = list
            prev = block_no
    return final_response


def createdb():
    """
    Creates a new SQLite database named 'normanpd.db' and sets up a table for incident data.
    """
    db_directory = 'resources'  
    db_file = os.path.join(db_directory, 'normanpd.db')  
    
    if not os.path.exists(db_directory):  
        os.makedirs(db_directory)  
    
    if os.path.exists(db_file): 
        os.remove(db_file)  
        
    conn = sqlite3.connect(db_file)  
    cursor = conn.cursor()  
    cursor.execute('''CREATE TABLE IF NOT EXISTS incidents (
                        incident_time TEXT,
                        incident_number TEXT,
                        incident_location TEXT,
                        nature TEXT,
                        incident_ori TEXT
                      );''')  
    conn.commit()  
    return conn  


def populatedb(db, incidents):
    """
    Inserts the extracted incident data into the SQLite database.
    """
    cursor = db.cursor()  
    cursor.executemany('''INSERT INTO incidents 
                          (incident_time, incident_number, incident_location, nature, incident_ori) 
                          VALUES (?, ?, ?, ?, ?);''', incidents)  
    db.commit()  


def read_nature_column(db_path):
    
    # Reads nature data, incident number, and incident location from the specified database and returns a list of tuples.
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT nature, incident_number, incident_location FROM incidents")
    nature_data = cursor.fetchall()
    conn.close()
    return nature_data


def read_incident_times(db_path='resources/normanpd.db'):
    
    # Reads incident time and number data from the specified database and returns a list of incident times and numbers.
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT incident_time, incident_number FROM incidents")
    incident_data = cursor.fetchall()
    conn.close()
    return incident_data



def calculate_day_and_time(incident_data):
    
    # For each incident_time, calculates the day of the week and the hour of the incident and includes the incident number.

    augmented_data = []
    for time_str, incident_number in incident_data:
        incident_time = datetime.strptime(time_str, "%m/%d/%Y %H:%M")
        day_of_week = incident_time.isoweekday() % 7 + 1
        hour_of_incident = incident_time.hour
        augmented_data.append((day_of_week, hour_of_incident, incident_number))
    return augmented_data


# Initialize an empty dictionary to store the final augmented data
def populate_augmented_map(augmented_data, nature_data, emsstat_map, location_ranks, nature_ranks, side_of_town_map, weather_map):
    augmented_map = {}
    for index, ((day_of_week, hour_of_incident, incident_number), (nature, _, location)) in enumerate(zip(augmented_data, nature_data)):
        ems_stat = emsstat_map.get(incident_number, 0)  # Get EMSSTAT status with a default of 0
        location_rank = location_ranks.get(location, None) # Location rank based on frequency, None if location is not ranked.
        incident_rank = nature_ranks.get(nature, None) # Nature rank based on frequency, None if nature is not ranked.
        side_of_town = side_of_town_map.get(location, "N/A") # Side of town, default to "N/A" if not determinable.
        weather_code = weather_map.get(incident_number, "N/A") # Weather condition at the time of the incident, default to "N/A" if missing.

        # Populate the augmented map with a comprehensive view of each incident.
        augmented_map[incident_number] = {
            "Day_of_the_Week": day_of_week,
            "Time_of_Day": hour_of_incident,
            "Weather": weather_code,
            "Location Rank": location_rank,
            "Side of Town": side_of_town,
            "Incident Rank": incident_rank,
            "Nature": nature,
            "EMSSTAT": ems_stat
        }
    return augmented_map


def get_locations(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT incident_location FROM incidents")
    locations = [location[0] for location in cursor.fetchall()]
    return locations


def get_nature(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT nature FROM incidents")
    nature = [nature[0] for nature in cursor.fetchall()]
    return nature

from collections import Counter

def calculate_location_rank(locations):
   
    # Count the occurrences of each location
    location_counter = Counter(locations)
    
    # Sort locations by frequency (descending) and then alphabetically
    sorted_locations = sorted(location_counter.items(), key=lambda x: (-x[1], x[0]))
    
    location_ranks = {}
    current_rank = 1  
    prev_count = -1  # Initialize with an impossible count
    same_rank_counter = 1  # Counts how many locations have the same rank for skipping after a tie

    for location, count in sorted_locations:
        if count != prev_count:
            current_rank = same_rank_counter
            prev_count = count
        location_ranks[location] = current_rank
        same_rank_counter += 1  # Always increment this, as it determines the next rank after a tie

    return location_ranks


def calculate_nature_rank(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT nature FROM incidents")
    natures = [nature[0] for nature in cursor.fetchall()]
    
    # Count the occurrences of each nature
    nature_counter = Counter(natures)
    
    # Sort natures by frequency
    sorted_natures = sorted(nature_counter.items(), key=lambda x: (-x[1], x[0]))
    
    nature_ranks = {}
    current_rank = 1  
    prev_count = None  # Placeholder for the count of the previous nature

    for nature, count in sorted_natures:
        # If this nature has the same count as the previous one, it gets the same rank
        if count == prev_count:
            nature_ranks[nature] = current_rank
        else:
            # If this is a new count, update the current rank and assign it to this nature
            nature_ranks[nature] = current_rank
            prev_count = count
            current_rank += 1  # Only increment rank if there was no tie
        
        # The next nature's rank is always 1 plus the number of natures processed so far
        
        current_rank = len(nature_ranks) + 1

    return nature_ranks


def main(urls_file):
    # Create a new SQLite database to store incident data.
    db = createdb()
    
    # Open the CSV file containing incident summary URLs and process each URL.
    with open(urls_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            url = row[0]
            # Download incident data from the URL and save it to the database.
            incident_data = fetchincidents(url)
            incidents = extractincidents(incident_data)
            populatedb(db, incidents)

    # Retrieve additional data from the database and other sources for analysis and augmentation.
    emsstat_map = get_emsstat_map('resources/normanpd.db')
    side_of_town_map = get_side_of_town_map('resources/normanpd.db')
    weather_map = get_weather_map('resources/normanpd.db')

    # Calculate location and nature ranks based on frequency of occurrence.
    locations = get_locations(db)
    location_ranks = calculate_location_rank(locations)
    natures = get_nature(db)
    nature_ranks = calculate_location_rank(natures)

    # Read incident time data and calculate day of the week and time of the incident.
    nature_data = read_nature_column('resources/normanpd.db')
    incident_times = read_incident_times('resources/normanpd.db')
    augmented_data = calculate_day_and_time(incident_times)

    # Populate an augmented map with comprehensive incident details for further analysis.
    augmented_map = populate_augmented_map(augmented_data, nature_data, emsstat_map, location_ranks, nature_ranks, side_of_town_map, weather_map)

    # Print the augmented map data in a formatted table for visualization and analysis.
    # print(f"{'Day of the Week':<15}\t{'Time of Day':<12}\t{'Weather':<8}\t{'Location Rank':<14}\t{'Side of Town':<12}\t{'Incident Rank':<14}\t{'Nature':<25}\t{'EMSSTAT':<10}")
    for key, value in augmented_map.items():
        print(f"{value['Day_of_the_Week']}\t{value['Time_of_Day']}\t{value['Weather']}\t{value['Location Rank']}\t{value['Side of Town']}\t{value['Incident Rank']}\t{value['Nature']}\t{value['EMSSTAT']}")

    # Close the database connection after processing is complete.
    db.close()

if __name__ == '__main__':
    # Parse command-line arguments to get the CSV file containing incident summary URLs.
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", type=str, required=True, help="CSV file containing incident summary URLs.")
    args = parser.parse_args()
    if args.urls:
        main(args.urls)

