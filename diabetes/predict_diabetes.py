# predict_diabetes.py

import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
import os

def calculate_bmi(weight_kg: float, height_m: float) -> float:
    if height_m <= 0 or weight_kg <= 0:
        raise ValueError("Height and weight must be positive numbers.")
    return round(weight_kg / (height_m ** 2), 2)


def calculate_lifestyle_score(physical_activity: str, dietary_habits: str) -> int:
    physical_activity_map = {"Low": 0, "Moderate": 1, "High": 2}
    dietary_habits_map = {"Unhealthy": 0, "Healthy": 1}
    return physical_activity_map[physical_activity] + dietary_habits_map[dietary_habits]


def calculate_genetic_risk_score(family_history: str, autoantibodies: str, genetic_markers: str) -> int:
    return int(family_history == "Yes") + int(autoantibodies == "Positive") + int(genetic_markers == "Positive")


def load_preprocessors_and_model(model_name: str = 'model/random_forest_model.pkl'):
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Load the Random Forest model
    with open(os.path.join(base_path, model_name), 'rb') as f:
        model = pickle.load(f)

    with open(os.path.join(base_path, 'model/scaler.pkl'), 'rb') as f:
        scaler = pickle.load(f)

    with open(os.path.join(base_path, 'model/label_encoders.pkl'), 'rb') as f:
        encoders = pickle.load(f)
        label_encoders = encoders['feature_encoders']
        target_encoder = encoders['target_encoder']

    with open(os.path.join(base_path, 'model/feature_columns.pkl'), 'rb') as f:
        feature_columns = pickle.load(f)

    return model, scaler, label_encoders, target_encoder, feature_columns


def predict_diabetes_type(user_input: dict, model, scaler, label_encoders, target_encoder, feature_columns):
    # Create a DataFrame from user input
    input_df = pd.DataFrame([user_input], columns=feature_columns)

    # Apply label encoding to categorical columns
    for col in label_encoders:
        input_df[col] = label_encoders[col].transform([input_df[col].iloc[0]])

    # Apply scaling to numerical columns
    numerical_cols = scaler.feature_names_in_ if hasattr(scaler, 'feature_names_in_') else input_df.columns.difference(label_encoders.keys())
    input_df[numerical_cols] = scaler.transform(input_df[numerical_cols])

    # Make prediction
    pred_label = model.predict(input_df)[0]  # Random Forest directly returns class labels
    pred_label = target_encoder.inverse_transform([pred_label])[0]
    return pred_label
