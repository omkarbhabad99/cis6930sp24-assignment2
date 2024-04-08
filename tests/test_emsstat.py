import pytest
from unittest.mock import patch
from ems import get_emsstat

# Test the get_emsstat function directly with sample data
def test_get_emsstat():
    sample_incidents = [
        (1, "3/1/2024 0:05", "2024-00014834", "4TH/SUNNYLANE", "Traffic Stop", "OK0140200"),
        (2, "3/1/2024 0:52", "2024-00004392", "2000 ANN BRANDEN BLVD", "Transfer/Interfacility", "EMSSTAT"),
        (3, "3/1/2024 1:41", "2024-00003324", "1523 MELROSE DR", "Unconscious/Fainting", "14005"),
        (4, "3/1/2024 1:41", "2024-00004393", "1523 MELROSE DR", "Falls", "EMSSTAT"),
    ]

    # Test get_emsstat function directly with an EMSSTAT incident
    assert get_emsstat(sample_incidents, 1, sample_incidents[1]) == 1, "EMSSTAT incident should return 1"

    # Test with a non-EMSSTAT incident that has the same location as an EMSSTAT incident
    assert get_emsstat(sample_incidents, 2, sample_incidents[2]) == 1, "Incident with same location as EMSSTAT should return 1"

    # Test with an incident not related to EMSSTAT and not sharing location with an EMSSTAT incident
    assert get_emsstat(sample_incidents, 0, sample_incidents[0]) == 0, "Non-EMSSTAT incident should return 0"
