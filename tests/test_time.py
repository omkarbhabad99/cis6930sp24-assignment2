from assignment2 import calculate_day_and_time
from datetime import datetime

def test_calculate_day_and_time():
    # Setup test data for March 1, 2024 which is a Friday
    test_data = [("3/1/2024 0:05", "2024-00014834"),  
                 ("3/1/2024 23:59", "2024-00014835")]  
    
    expected_result = [(6, 0, "2024-00014834"),
                       (6, 23, "2024-00014835")]
    
    # Run the calculate_day_and_time function
    result = calculate_day_and_time(test_data)
    
    # Assert the result matches the expected result
    assert result == expected_result, f"Expected {expected_result}, got {result}"
