
from pathlib import Path
import pandas as pd

# Locate the dataset from the project folder
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "ai4i2020.csv"

# Load the dataset
df = pd.read_csv(DATA_PATH)

# Display basic information
print("\n=== OPSPILOT AI: DATASET OVERVIEW ===")
print("Total rows:", df.shape[0])
print("Total columns:", df.shape[1])

print("\n=== COLUMN NAMES ===")
print(df.columns.tolist())

print("\n=== FIRST FIVE ROWS ===")
print(df.head())

print("\n=== MISSING VALUES ===")
print(df.isnull().sum())

print("\n=== MACHINE FAILURE DISTRIBUTION ===")
print(df["Machine failure"].value_counts())


# Select the features for machine learning
feature_columns = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]

X = df[feature_columns]
y = df["Machine failure"]

print("\n=== MACHINE LEARNING FEATURES ===")
print(X.head())

print("\n=== TARGET LABELS ===")
print(y.value_counts())

print("\n=== FEATURE MATRIX SHAPE ===")
print(X.shape)

print("\n=== TARGET SHAPE ===")
print(y.shape)



from sklearn.model_selection import train_test_split

# First split: 80% development, 20% final test
X_dev, X_test, y_dev, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Second split: 60% training, 20% validation
X_train, X_val, y_train, y_val = train_test_split(
    X_dev,
    y_dev,
    test_size=0.25,
    random_state=42,
    stratify=y_dev
)

print("\n=== OPSPILOT AI DATASET SPLIT ===")
print("Training records:", len(X_train))
print("Validation records:", len(X_val))
print("Testing records:", len(X_test))


from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Build a machine learning pipeline
model = make_pipeline(
    StandardScaler(),
    LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    )
)

# Train the model using training data only
print("\n=== TRAINING OPSPILOT AI BASELINE MODEL ===")

model.fit(X_train, y_train)

print("Model training completed successfully!")

# Make predictions on unseen test data
y_pred = model.predict(X_test)

print("\n=== FIRST PREDICTIONS ===")
print("Predicted:", y_pred[:10])
print("Actual:   ", y_test.iloc[:10].to_numpy())


from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

print("\n=== OPSPILOT AI BASELINE MODEL EVALUATION ===")

print("Accuracy:", round(accuracy_score(y_test, y_pred), 4))
print("Precision:", round(precision_score(y_test, y_pred, zero_division=0), 4))
print("Recall:", round(recall_score(y_test, y_pred, zero_division=0), 4))
print("F1 Score:", round(f1_score(y_test, y_pred, zero_division=0), 4))

print("\n=== CONFUSION MATRIX ===")
print(confusion_matrix(y_test, y_pred))

print("\n=== CLASSIFICATION REPORT ===")
print(classification_report(y_test, y_pred, zero_division=0))


from sklearn.ensemble import RandomForestClassifier

# Create our Random Forest model
rf_model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

print("\n=== TRAINING RANDOM FOREST MODEL ===")

# Train using the same training dataset
rf_model.fit(X_train, y_train)

print("Random Forest training completed!")

# Generate predictions
rf_pred = rf_model.predict(X_test)

print("\n=== RANDOM FOREST EVALUATION ===")

print("Accuracy:", round(accuracy_score(y_test, rf_pred), 4))
print("Precision:", round(precision_score(y_test, rf_pred, zero_division=0), 4))
print("Recall:", round(recall_score(y_test, rf_pred, zero_division=0), 4))
print("F1 Score:", round(f1_score(y_test, rf_pred, zero_division=0), 4))

print("\n=== RANDOM FOREST CONFUSION MATRIX ===")
print(confusion_matrix(y_test, rf_pred))

print("\n=== RANDOM FOREST CLASSIFICATION REPORT ===")
print(classification_report(y_test, rf_pred, zero_division=0))


# STEP 6.4.2: Analyze failure prediction probabilities

# Generate probabilities using validation data
rf_probabilities = rf_model.predict_proba(X_val)[:, 1]

print("\n=== RANDOM FOREST FAILURE PROBABILITIES ===")

print("First 10 failure probabilities:")
print(rf_probabilities[:10])

print("\n=== VALIDATION SET ANALYSIS ===")
print("Total validation records:", len(X_val))
print("Actual failures:", y_val.sum())

# Count predictions above different thresholds
for threshold in [0.3, 0.5, 0.7]:
    predicted_failures = (rf_probabilities >= threshold).sum()

    print(
        f"Threshold {threshold}: "
        f"{predicted_failures} predicted failures"
    )

# STEP 6.4.3: Compare prediction thresholds

from sklearn.metrics import precision_score, recall_score, f1_score

print("\n=== OPSPILOT AI THRESHOLD COMPARISON ===")

thresholds = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80]

best_threshold = None
best_f1 = -1

for threshold in thresholds:
    predictions = (rf_probabilities >= threshold).astype(int)

    precision = precision_score(
        y_val, predictions, zero_division=0
    )
    recall = recall_score(
        y_val, predictions, zero_division=0
    )
    f1 = f1_score(
        y_val, predictions, zero_division=0
    )

    print(
        f"Threshold: {threshold:.2f} | "
        f"Precision: {precision:.3f} | "
        f"Recall: {recall:.3f} | "
        f"F1: {f1:.3f}"
    )

    if f1 > best_f1:
        best_f1 = f1
        best_threshold = threshold

print("\n=== BEST VALIDATION THRESHOLD ===")
print("Threshold:", best_threshold)
print("F1 Score:", round(best_f1, 4))


# STEP 6.4.4: Compare default and optimized thresholds

from sklearn.metrics import confusion_matrix

print("\n=== OPSPILOT AI THRESHOLD PERFORMANCE ===")

for threshold in [0.50, best_threshold]:
    predictions = (rf_probabilities >= threshold).astype(int)

    print(f"\nThreshold: {threshold:.2f}")

    print("Precision:", round(
        precision_score(y_val, predictions, zero_division=0), 4
    ))

    print("Recall:", round(
        recall_score(y_val, predictions, zero_division=0), 4
    ))

    print("F1 Score:", round(
        f1_score(y_val, predictions, zero_division=0), 4
    ))

    tn, fp, fn, tp = confusion_matrix(
        y_val, predictions, labels=[0, 1]
    ).ravel()

    print("Correctly detected failures:", tp)
    print("Missed failures:", fn)
    print("False alarms:", fp)
    print("Correctly identified normal cases:", tn)


# STEP 6.4.5: Save the trained ML model

import joblib
from pathlib import Path

# Create a folder for trained models
MODEL_DIR = Path(__file__).resolve().parent / "saved_models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Define model file location
MODEL_PATH = MODEL_DIR / "random_forest_model.joblib"

# Save the trained Random Forest model
joblib.dump(rf_model, MODEL_PATH)

# Save model configuration separately
CONFIG_PATH = MODEL_DIR / "model_config.joblib"

model_config = {
    "model_name": "RandomForestClassifier",
    "model_version": "0.1.0",
    "threshold": float(best_threshold),
    "feature_columns": feature_columns,
    "dataset": "AI4I 2020",
    "status": "experimental"
}

joblib.dump(model_config, CONFIG_PATH)

print("\n=== OPSPILOT AI MODEL SAVED ===")
print("Model saved to:", MODEL_PATH)
print("Configuration saved to:", CONFIG_PATH)
print("Selected threshold:", best_threshold)












