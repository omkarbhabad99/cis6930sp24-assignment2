
# CIS 6930 Data Engineering - Assignment 2

## Name 
Omkar Sunil Bhabad

## Description
This project which is an extension of `asssignment0` is designed to fetch, process, and analyze incident report summaries from the Norman Police Department. By downloading PDF reports, extracting data, and storing it in a structured SQLite database, the project enables easy access to public safety information as its potential future use case. It leverages text extraction techniques and APIs to determine weather conditions and geographical information related to incidents.

## Installation
1. Ensure Python 3.x and Pipenv are installed on your system.
2. Clone the project repository.
3. Run `pipenv install` to create a virtual environment and install the required dependencies. You might need to run the following commands if not already installed.
   Run `pip install PyMuPDF`
   Run `pip install requests`
   Run `pip install googlemaps`
   Run `pip install PyMuPDF requests googlemaps`

4. Activate the virtual environment using `pipenv shell`.
5. To execute the script, use the following command: `pipenv run python assignment2.py --urls files.csv` .

## Components

### assignment2.py
- Serves as the main entry point for the program.
- Manages downloading PDFs, parsing incident data, and populating the database.

### side.py
- Contains functionality to determine the side of town for each incident.

### weather.py
- Utilizes external weather APIs to fetch weather conditions related to the incidents.

### ems.py
- calculates EMMSTAT of the incident by comparing addresses.

# Function Descriptions

## `fetchincidents`
**Purpose**: Automates the downloading of PDF files containing incident reports from specified URLs.

**Process**: Uses Python's `urllib` library to send HTTP requests to the given URLs and saves the content as temporary files.

**Output**: The local file system path to the downloaded PDF files.

## `extractincidents`
**Purpose**: Extracts structured incident data from downloaded PDF files.

**Process**: Leverages the PyMuPDF library to read text in PDFs, identifying incidents based on layout and formatting.

**Output**: A list of tuples, with each tuple containing structured data for one incident report.

## `createdb`
**Purpose**: Initiates the creation of a new SQLite database for structured storage of incident data.

**Process**: Utilizes Python's `sqlite3` library to create a database file and set up the necessary schema with appropriate tables and columns.

**Output**: A database connection object for further data manipulation.

## `populatedb`
**Purpose**: Inserts structured incident data into the SQLite database.

**Process**: Executes SQL `INSERT` statements for each incident tuple to populate the database.

**Output**: The database filled with incident records, ready for analysis and querying.

## `process_emsstat`
**Purpose**: Identifies the EMSSTAT status for each incident within the database.

**Process**: Examines the `incident_ori` field of each incident to determine if it is marked as EMSSTAT.

**Output**: A list of boolean values corresponding to the EMSSTAT status of each incident.

## `calculate_day_and_time`
**Purpose**: Computes the day of the week and time of day for each incident.

**Process**: Converts `incident_time` strings into `datetime` objects to extract the day and hour of incidents.

**Output**: An enhanced list of incident tuples, each augmented with day of the week and time of day information.

## `calculate_nature_rank`
**Purpose**: Ranks each incident type by the frequency of its occurrence.

**Process**: Counts occurrences of each unique incident nature, sorts them, and assigns a rank based on frequency.

**Output**: A dictionary linking each incident nature to its rank according to occurrence frequency.

## `calculate_location_rank`
**Purpose**: Ranks each incident location by the frequency of incidents that occur there.

**Process**: Similar to `calculate_nature_rank`, it tallies and ranks locations by incident count.

**Output**: A dictionary that maps each location to its incident frequency rank.

## `geocode_location`
**Purpose**: Geocodes a single location using the Google Maps API to determine its latitude and longitude.

**Process**: Utilizes the Google Maps API to geocode the given location string appended with 'Norman, OK'. Extracts the latitude and longitude from the API response and calculates the side of town using the get_side_of_town function.

**Output**: Returns a tuple containing the original location string and its determined side of town.

## `get_side_of_town`
**Purpose**: Determines the side of town based on the latitude and longitude coordinates of a location.

**Process**: Calculates the angle between the location coordinates and the central point of Norman, Oklahoma. Divides the area surrounding Norman into eight sectors based on the calculated angle and assigns a side of town accordingly.

**Output**: Returns a string representing the side of town where the location is situated.

## `fetch_weather_data_for_location`
**Purpose**: Fetches weather data for a specific incident location using the Open-Meteo API.

**Process**: Converts the incident time string to a datetime object. Geocodes the location using the Google Maps API to obtain latitude and longitude coordinates. Constructs parameters for the API request, including latitude, longitude, start date, end date, and desired weather information (hourly weather code). Sends a request to the Open-Meteo API and parses the response to extract the hourly weather code for the incident date.

**Output**: Returns a tuple containing the incident number and the corresponding hourly weather code, or "Not Available" if an error occurs.

## `get_weather_map`
**Purpose**: Retrieves weather data for all incidents in the database and creates a map of incident numbers to hourly weather codes.

**Process**: Retrieves incident details from the specified database using get_incident_details. Utilizes ThreadPoolExecutor to concurrently fetch weather data for each incident location using fetch_weather_data_for_location. Maps each incident number to its corresponding hourly weather code in the weather_map.

**Output**:  Returns a dictionary (weather_map) mapping incident numbers to their respective hourly weather codes.

## `populate_augmented_map`
**Purpose**: Populates a map with comprehensive incident details, combining temporal, spatial, and categorical information.

**Process**: Iterates over incident data and retrieves additional details such as EMSSTAT status, location rank, nature rank, side of town, and weather condition for each incident. These details are structured into a dictionary format and added to the map.

**Output**: Returns the populated map, where each incident number is associated with a dictionary containing various incident details.


## Output
The script outputs a tab-separated list of augmented data entries including day of the week, time of day, weather conditions, location rank, side of town, incident rank, nature of the incident, and EMSSTAT status.

## Known Bugs and Assumptions
- The script assumes PDF files follow a consistent format.
- Weather data is fetched from an external API; discrepancies in weather codes may occur.
- The side of town calculation is based on a static center point, which may not reflect actual city boundaries.

## Tests
Unit tests are included in the `tests` directory. 

1. **test_dayofweek** : The test case for the calculate_day_and_time function validates its ability to accurately determine the custom day of the week based on the provided incident timestamps. Using pytest parametrization, the test covers a sample timestamp corresponding to a known day of the week, ensuring that the function returns the expected custom day of the week for that timestamp. If the calculated day matches the expected value, the test case passes, affirming the correctness of the function's implementation.

2. **test_emsstat** : The test case for the get_emsstat function directly validates its behavior with sample incident data. Using pytest and the unittest.mock.patch decorator, the test directly calls the function with various scenarios: an EMSSTAT incident, a non-EMSSTAT incident sharing the same location as an EMSSTAT incident, and a non-EMSSTAT incident with a different location. For each scenario, the test verifies that the function correctly identifies EMSSTAT incidents and returns the expected result. If the function behaves as expected in all scenarios, the test case passes, confirming the correctness of the get_emsstat function.

3. **test_nature** : 
test_calculate_nature_rank_basic: Checks ranking behavior without ties in nature frequencies.
test_calculate_nature_rank_with_ties: Verifies ranking when ties occur in nature frequencies.

4. **test_time.py** : The test_calculate_day_and_time function in the test suite verifies the correctness of the calculate_day_and_time function from assignment2. It prepares test data representing incidents on March 1, 2024, at the day's start and end, along with the expected output. This test ensures that the function accurately computes the day of the week and incident hour for each timestamp, reporting any inconsistencies.

5. **test_weather.py** : In test_fetch_weather_data_for_location_simple, a mock response is set up for geocoding and weather API calls. The test verifies that the fetch_weather_data_for_location function correctly handles a mocked incident and returns the expected weather code.
In test_get_weather_map_simple, the get_weather_map function is tested with minimal setup. Mock return values are provided, simulating a call to get_incident_details and fetch_weather_data_for_location. The test ensures that get_weather_map generates the expected weather map based on the mocked data.

## Resources
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
- [SQLite](https://www.sqlite.org/index.html)
- [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)



