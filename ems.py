# emsstat.py

import sqlite3

def get_incident_details(db_path):
    
    # Fetches all incidents from the database.

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, incident_time, incident_number, incident_location, nature, incident_ori FROM incidents")
    incidents = cursor.fetchall()
    conn.close()
    return incidents

def get_emsstat(incidents, index, incident):
    
    # Determine if an incident is related to EMSSTAT, including checks for up to 5 entries before and after.
    
    if incident[5] == "EMSSTAT":
        return 1
    else:
        # Extend the range to check up to 5 entries before and after the current incident
        for i in range(max(0, index - 5), min(len(incidents), index + 6)):  # Adjusted indices
            if i != index and incidents[i][3] == incident[3] and incidents[i][5] == "EMSSTAT":
                return 1
    return 0


def get_emsstat_map(db_path='resources/normanpd.db'):
    
    # Creates a map of incident numbers to their EMSSTAT status.
    
    incidents = get_incident_details(db_path)
    emsstat_map = {}
    for index, incident in enumerate(incidents):
        emsstat_map[incident[2]] = get_emsstat(incidents, index, incident)
    return emsstat_map

if __name__ == "__main__":
    emsstat_map = get_emsstat_map()
    for incident_number, emsstat_status in emsstat_map.items():
        print(f"Incident Number: {incident_number}, EMSSTAT: {emsstat_status}")
