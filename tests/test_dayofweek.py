import pytest
from assignment2 import calculate_day_and_time  # Adjust this import path

# Helper function to convert datetime weekday to custom day of the week
def datetime_to_custom_dayofweek(datetime_obj):
    
    return ((datetime_obj.weekday() + 1) % 7) + 1

# Test case with datetime string and expected custom day of the week
test_cases = [
    ("4/7/2024 01:30", 1),  # 2024-04-07 is a Sunday
]

@pytest.mark.parametrize("timestamp, expected_custom_day", test_cases)
def test_calculate_day_of_week(timestamp, expected_custom_day):
    calculated_data = calculate_day_and_time([(timestamp, "dummy_incident_number")])
    
    for _, calculated_day_of_week, _ in calculated_data:
        assert calculated_day_of_week == expected_custom_day, f"Expected {expected_custom_day} for timestamp '{timestamp}', got {calculated_day_of_week}"
