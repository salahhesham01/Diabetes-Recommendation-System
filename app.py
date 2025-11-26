import streamlit as st
from ui_style import set_page_style
from nutrition.nutrition_main import run_nutrition_page
from diabetes.predict_diabetes_main import run_prediction_page


set_page_style()

if "page" not in st.session_state:
    st.session_state.page = "main"

if st.session_state.page == "main":
    run_nutrition_page()
elif st.session_state.page == "predict":
    run_prediction_page()
