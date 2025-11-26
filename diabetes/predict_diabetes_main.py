import streamlit as st
import pandas as pd
from .predict_diabetes import (
    calculate_bmi, calculate_lifestyle_score, calculate_genetic_risk_score,
    load_preprocessors_and_model, predict_diabetes_type
)

def run_prediction_page():
    st.title("Predict Your Diabetes Type")
    
    st.write("Please fill out the following information:")

    # Create tabs for better organization
    tab1, tab2, tab3 = st.tabs(["👤 Physical Profile", "❤️ Health Status", "👨‍🦯 Lifestyle"])

    with tab1:
        st.header("Physical Profile")
        st.write("Enter your basic physical details.")
        age = st.number_input("Age", min_value=1, max_value=120, value=50)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=0) # Added Gender input
        weight_kg = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0, value=80.0)
        height_m = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.7)

    with tab2:
        st.header("Health Status")
        st.write("Provide details about your current health and medical history.")
        insulin = st.number_input("Insulin Levels", min_value=0.0, value=15.0)
        blood_pressure = st.number_input("Blood Pressure", min_value=0, value=120)
        cholesterol = st.number_input("Cholesterol Levels", min_value=0, value=180)
        glucose = st.number_input("Blood Glucose Levels", min_value=0, value=100)
        gtt = st.selectbox("Glucose Tolerance Test", ["Normal", "Abnormal"], index=0)
        cystic = st.selectbox("Cystic Fibrosis Diagnosis", ["Yes", "No"], index=1)
        autoantibodies = st.selectbox("Autoantibodies", ["Positive", "Negative"], index=1)
        genetic_markers = st.selectbox("Genetic Markers", ["Positive", "Negative"], index=1)
        family_history = st.selectbox("Family History of Diabetes", ["Yes", "No"], index=1)
        genetic_test = st.selectbox("Genetic Testing", ["Positive", "Negative"], index=1)

    with tab3:
        st.header("👨‍🦯 Lifestyle")
        st.write("Share information about your lifestyle habits and family history.")
        smoking = st.selectbox("Smoking Status", ["Smoker", "Non-Smoker"], index=1)
        activity = st.selectbox("Physical Activity", ["Low", "Moderate", "High"], index=1)
        diet = st.selectbox("Dietary Habits", ["Unhealthy", "Healthy"], index=1)
        waist = st.number_input("Waist Circumference (cm)", min_value=0, value=85)
        early_symptoms = st.selectbox("Early Onset Symptoms", ["Yes", "No"], index=1)
 

    # Buttons outside the tabs for consistent placement
    st.markdown("---") # Add a separator for visual clarity
    col1, col2 = st.columns(2) # Use columns to place buttons side-by-side

    with col1:
        if st.button("Predict Diabetes Type"):
            bmi = calculate_bmi(weight_kg, height_m)
            lifestyle_score = calculate_lifestyle_score(activity, diet)
            genetic_risk = calculate_genetic_risk_score(family_history, autoantibodies, genetic_markers)

            user_input = {
                "Insulin Levels": insulin,
                "Age": age,
                "BMI": bmi,
                "Blood Pressure": blood_pressure,
                "Cholesterol Levels": cholesterol,
                "Waist Circumference": waist,
                "Blood Glucose Levels": glucose,
                "Lifestyle_Score": lifestyle_score,
                "Genetic_Risk_Score": genetic_risk,
                "Smoking Status": smoking,
                "Glucose Tolerance Test": gtt,
                "Cystic Fibrosis Diagnosis": cystic,
                "Genetic Testing": genetic_test,
                "Early Onset Symptoms": early_symptoms,
                "Gender": gender # Include gender in the input dictionary
            }

            model, scaler, label_encoders, target_encoder, feature_columns = load_preprocessors_and_model()
            predicted_type = predict_diabetes_type(user_input, model, scaler, label_encoders, target_encoder, feature_columns)

            st.success(f"Predicted Diabetes Type: {predicted_type}")

    with col2:
        if st.button("← Go Back"):
            st.session_state.page = "main"
            st.rerun()

