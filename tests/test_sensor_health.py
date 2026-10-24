
from routers.sensors import (
    assess_temperature,
    assess_vibration,
    assess_pressure,
    assess_overall_health,
)


def test_temperature_assessment():
    assert assess_temperature(75.5) == "NORMAL"
    assert assess_temperature(85.5) == "WARNING"
    assert assess_temperature(105.5) == "CRITICAL"
    assert assess_temperature(None) == "UNKNOWN"


def test_vibration_assessment():
    assert assess_vibration(2.3) == "NORMAL"
    assert assess_vibration(3.5) == "WARNING"
    assert assess_vibration(5.5) == "CRITICAL"
    assert assess_vibration(None) == "UNKNOWN"


def test_pressure_assessment():
    assert assess_pressure(6.2) == "NORMAL"
    assert assess_pressure(8.5) == "WARNING"
    assert assess_pressure(10.5) == "CRITICAL"
    assert assess_pressure(None) == "UNKNOWN"


def test_overall_health_assessment():
    assert assess_overall_health(
        "NORMAL", "NORMAL", "NORMAL"
    ) == "NORMAL"

    assert assess_overall_health(
        "NORMAL", "WARNING", "NORMAL"
    ) == "WARNING"

    assert assess_overall_health(
        "CRITICAL", "WARNING", "NORMAL"
    ) == "CRITICAL"

    assert assess_overall_health(
        "UNKNOWN", "UNKNOWN", "UNKNOWN"
    ) == "UNKNOWN"


