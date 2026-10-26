
from fastapi.testclient import TestClient
from main import app
from ml.predict import predict_failure

client = TestClient(app)


def test_prediction_function():
    """Check that our trained ML model returns valid results."""

    result = predict_failure(
        air_temperature=298.1,
        process_temperature=308.6,
        rotational_speed=1551,
        torque=42.8,
        tool_wear=0
    )

    assert isinstance(result["predicted_failure"], bool)
    assert 0 <= result["failure_score"] <= 1
    assert 0 <= result["threshold"] <= 1
    assert result["model_status"] == "experimental"


def test_prediction_requires_authentication():
    """Check that unauthenticated API requests are rejected."""

    response = client.post(
        "/predictions/failure",
        json={
            "air_temperature": 298.1,
            "process_temperature": 308.6,
            "rotational_speed": 1551,
            "torque": 42.8,
            "tool_wear": 0
        }
    )

    assert response.status_code == 401


