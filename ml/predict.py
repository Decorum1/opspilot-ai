
from pathlib import Path

import joblib
import pandas as pd

# Locate saved machine learning files
MODEL_DIR = Path(__file__).resolve().parent / "saved_models"

MODEL_PATH = MODEL_DIR / "random_forest_model.joblib"
CONFIG_PATH = MODEL_DIR / "model_config.joblib"

# Load our locally trained model and configuration
model = joblib.load(MODEL_PATH)
config = joblib.load(CONFIG_PATH)


def predict_failure(
    air_temperature: float,
    process_temperature: float,
    rotational_speed: float,
    torque: float,
    tool_wear: float
):
    # Prepare data using the exact training feature names
    input_data = pd.DataFrame([{
        "Air temperature [K]": air_temperature,
        "Process temperature [K]": process_temperature,
        "Rotational speed [rpm]": rotational_speed,
        "Torque [Nm]": torque,
        "Tool wear [min]": tool_wear
    }])

    # Ensure the correct feature order
    input_data = input_data[config["feature_columns"]]

    # Generate the failure-class score
    probability = float(
        model.predict_proba(input_data)[0][1]
    )

    # Apply the selected validation threshold
    threshold = float(config["threshold"])

    predicted_failure = probability >= threshold

    return {
        "predicted_failure": bool(predicted_failure),
        "failure_score": round(probability, 4),
        "threshold": threshold,
        "model_version": config["model_version"],
        "model_status": "experimental"
    }


