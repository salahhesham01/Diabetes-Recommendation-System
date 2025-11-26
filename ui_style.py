import base64
import streamlit as st

def set_page_style():
    """Applies minimal and modern CSS styles for a clean UI."""

    # --- Optional Background Image ---
    try:
        with open("background.jpg", "rb") as image:
            base64_image = base64.b64encode(image.read()).decode()
        background = f"""
        <style>
        [data-testid="stApp"] {{
            background-image: url("data:image/png;base64,{base64_image}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """
    except FileNotFoundError:
        background = """
        <style>
        [data-testid="stApp"] {
            background-color: #f4f4f4;
        }
        </style>
        """
    st.markdown(background, unsafe_allow_html=True)

    # --- Base UI Styles + Header Color ---
    base_styles = """
    <style>
    /* HEADERS AND PARAGRAPHS */
    h1 {
        color: black !important;
    }
    h2 {
        color: black !important;
    }



    p {
        color: black !important;
    }

    /* INPUTS */
    div[data-testid="stNumberInput"],
    div[data-testid="stSelectbox"],
    div[data-testid="stTextInput"] {
        background: white;
        border: 1px solid #ccc;
        border-radius: 6px;
        padding: 8px;
    }

    /* LABELS */
    label[data-testid="stWidgetLabel"] {
        font-size: 0.9rem;
        color: #333;
        font-weight: 600;
    }

    /* INPUT TEXT */
    input {
        font-size: 1rem;
        color: #333;
    }

    /* BUTTONS */
    button[kind="primary"] {
        background-color: #0078d4;
        color: white;
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 1rem;
        border: none;
    }
    button[kind="primary"]:hover {
        background-color: #005fa3;
    }

    /* TABS */
    button[data-baseweb="tab"] {
        background: none;
        border: none;
        color: #555;
        font-weight: 500;
        font-size: 0.95rem;
        padding: 8px 12px;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom: 2px solid #0078d4;
        color: #0078d4;
        font-weight: 600;
    }
    </style>
    """
    st.markdown(base_styles, unsafe_allow_html=True)
