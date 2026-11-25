
from datetime import datetime, timezone

import pytest

from main import transform_weather


def test_transform_weather():
    # Beispielantwort der Wetter-API
    sample_data = {
        "current": {
            "time": "2026-11-24T10:30",
            "temperature_2m": 2.3,
            "relative_humidity_2m": 78,
        }
    }

    result = transform_weather(sample_data)

    assert result["city"] == "Berlin"
    assert result["temperature_c"] == 2.3
    assert result["humidity_percent"] == 78
    assert result["observed_at"] == datetime(
        2026, 11, 24, 10, 30, tzinfo=timezone.utc
    )


def test_missing_temperature():
    sample_data = {
        "current": {
            "time": "2026-11-24T10:30",
            "relative_humidity_2m": 78,
        }
    }

    with pytest.raises(KeyError):
        transform_weather(sample_data)
