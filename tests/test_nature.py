import pytest
from unittest.mock import Mock
from assignment2 import calculate_nature_rank

def test_calculate_nature_rank_basic():
    # Simulated input and expected output
    natures_input = ["Theft", "Assault", "Theft", "Robbery", "Assault", "Theft"]
    expected_output = {"Theft": 1, "Assault": 2, "Robbery": 3}

    class MockCursor:
        def execute(self, query):
            pass
        def fetchall(self):
            return [(nature,) for nature in natures_input]

    mock_conn = Mock()
    mock_conn.cursor.return_value = MockCursor()

    actual_output = calculate_nature_rank(mock_conn)
    assert actual_output == expected_output, f"Expected {expected_output}, but got {actual_output}"

def test_calculate_nature_rank_with_ties():
    natures_input = ["Theft", "Assault", "Robbery", "Assault", "Robbery"]
    # Updated expected output to reflect that 'Robbery' gets a rank of 2 instead of 1
    expected_output = {"Assault": 1, "Robbery": 2, "Theft": 3}

    class MockCursor:
        def execute(self, query):
            pass
        def fetchall(self):
            return [(nature,) for nature in natures_input]

    mock_conn = Mock()
    mock_conn.cursor.return_value = MockCursor()

    actual_output = calculate_nature_rank(mock_conn)
    assert actual_output == expected_output, f"Expected {expected_output}, but got {actual_output}"

