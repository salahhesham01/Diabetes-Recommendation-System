import streamlit as st
import pandas as pd
from time import sleep

# Assuming these files are in the same directory or accessible
from .calorie_calc import calculate_calories
from .diet_logic import select_diet
from .meal_filter import filter_meals, rank_meals_cosine
from .meal_recommender import recommend_nutrition_plan
from .plot_utils import plot_nutrients
from .rules import recommend_diet_with_expert_system
# --- Main Streamlit App ---
def run_nutrition_page():
    st.title("🍓DiaPal")
    st.markdown("Personalized nutrition plans for diabetes management")

    # Tabs for inputs
    tab1, tab2, tab3 = st.tabs(["👤 Physical Profile", "❤️ Health Status", "🎯 Goals & Lifestyle"])

    with tab1:
        age = st.number_input("Age", min_value=18, max_value=100, value=50)
        gender = st.selectbox("Gender", ["M", "F"], index=0)
        weight_kg = st.number_input("Weight (kg)", min_value=30, max_value=200, value=80)
        height_cm = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)

    with tab2:
        diabetes_type_map = {"Prediabetes": "0", "Type 1": "1", "LADA": "2", "Type 2": "3", "MODY": "4"}
        diabetes_type_label = st.selectbox("Diabetes Type", list(diabetes_type_map.keys()), index=3)
        diabetes_type = diabetes_type_map[diabetes_type_label]

        if st.button("I don't know my diabetes type (Predict it)"):
            st.session_state.page = "predict"
            st.rerun()

        blood_pressure = st.number_input("Blood Pressure (Systolic, mg/dL)", value=120)
        blood_glucose = st.number_input("Average Blood Glucose (mg/dL)", value=100)

    with tab3:
        activity_level = st.selectbox("Activity Level", ["Lightly Active", "Moderately Active", "Very Active"], index=1)
        dietary_habits = st.selectbox("Current Dietary Habits", ["Healthy", "UnHealthy"], index=0)
        goal = st.selectbox("Primary Goal", ["Blood sugar control", "Weight loss"], index=0)

    st.divider()

    # --- Diet Recommendation Selection ---
    st.subheader("🥗 Diet Selection")
    diet_choice = st.radio(
        "How do you want to select your diet?",
        ["Recommend diet (Expert system)", "Choose diet manually"],
        horizontal=True,
        index=0
    )
    manual_diet = None
    if diet_choice == "Choose diet manually":
        manual_diet = st.selectbox("Select Diet", ["Low-carb", "Mediterranean", "Keto", "Moderate-carb", "Dash"])

    if st.button("🚀 Generate My Nutrition Plan", use_container_width=True):
        bmi = weight_kg / ((height_cm / 100) ** 2)
        user_profile = {
            "age": age, "gender": gender, "weight_kg": weight_kg, "height_cm": height_cm,
            "diabetes_type": diabetes_type, "activity_level": activity_level,
            "Blood Glucose Levels": blood_glucose, "goal": goal, "dietary_habits": dietary_habits,
            "Blood Pressure": blood_pressure,
            "bmi": bmi,
            "blood_glucose": blood_glucose,
            "blood_pressure": blood_pressure
        }
        user_goal = {
            "Blood sugar control": {"calorie_adjustment": 0},
            "Weight loss": {"calorie_adjustment": -300},
        }[goal]
        calorie_target = calculate_calories(user_profile, user_goal)

        with st.spinner('Building your personalized plan... This may take a moment.'):
            recommended_diet = manual_diet
            if diet_choice == "Recommend diet (Expert system)":
                recommended_diet = recommend_diet_with_expert_system(user_profile)

            user_diet = select_diet(user_profile, diet_choice, recommended_diet, calorie_target)
            filtered_meals = filter_meals(user_profile, user_goal, user_diet)
            ranked_meals = rank_meals_cosine(filtered_meals, user_diet)
            plan, total_calories = recommend_nutrition_plan(ranked_meals, calorie_target, user_diet)
            sleep(1)

        st.success("Your personalized nutrition plan is ready!")

        col1, col2 = st.columns(2)
        col1.metric(label="🎯 Daily Calorie Target", value=f"{calorie_target} kcal")
        if recommended_diet:
            col2.metric(label="✨ Recommended Diet", value=recommended_diet)

        st.divider()

        if plan:
            st.subheader(f"Your Daily Meal Plan ({int(total_calories)} kcal)")
            for meal in plan:
                with st.container():
                    st.markdown(f'<div class="meal-card">', unsafe_allow_html=True)
                    st.subheader(f"{meal['type']}: {meal['meal_name']}")
                    st.write(f"**Cuisine:** {meal['cuisine']}")
                    st.write(
                        f"**Macros:** "
                        f"Calories: {meal['calories']} kcal | "
                        f"Carbs: {meal['carbs_g']}g | "
                        f"Protein: {meal['protein_g']}g | "
                        f"Fat: {meal['fat_g']}g"
                    )
                    st.progress(meal['calories'] / calorie_target, text=f"{int((meal['calories']/calorie_target)*100)}% of Daily Calories")
                    st.markdown('</div>', unsafe_allow_html=True)

            fig = plot_nutrients(plan)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No meals found matching your criteria. Please try adjusting your goals or diet selection.")
