import streamlit as st 
import pandas as pd
from extract_features import extract_features

# 🔧 Streamlit page config
st.set_page_config(
    page_title="OYSCATECH - Anti-Phishing System",
    layout="centered"
)

# 🎨 Add background and school name at the top
def add_custom_style():
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url("https://images.unsplash.com/photo-1521791136064-7986c2920216");
                background-size: cover;
                background-attachment: fixed;
                background-repeat: no-repeat;
                background-position: center;
            }}
            .school-header {{
                font-size: 36px;
                font-weight: bold;
                text-align: center;
                color: white;
                background-color: rgba(0,0,0,0.6);
                padding: 15px;
                border-radius: 12px;
                margin-bottom: 20px;
            }}
        </style>
        <div class="school-header">OYSCATECH - Oyo State College of Agriculture and Technology <h6> by hopzee</h6></div>
        """,
        unsafe_allow_html=True
    )

# Call the styling
add_custom_style()

# 🔐 Title and input
st.title("🔐 Anti-Phishing URL Detector")

url_input = st.text_input("🔗 Enter a URL:")

if url_input:
    features = extract_features(url_input)
    df = pd.DataFrame([features])

    is_legit = features["is_exact_legit"]
    homoglyph = features["has_homoglyph"]

    # ✅ Styled result display
    if is_legit:
        result = "Legitimate ✅"
        color = "#d4edda"       # Light green
        text_color = "#155724"  # Dark green text
    else:
        result = "Phishing ❌"
        color = "#ab101d"       # Custom red
        text_color = "#ffffff"  # White text for red background

    st.markdown(
        f"""
        <div style="background-color: {color}; color: {text_color}; padding: 15px; 
                    border-radius: 10px; font-size: 20px; font-weight: bold; 
                    text-align: center; margin-top: 20px;">
            🧠 Prediction: {result}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ✅ Styled Homoglyph result in black
    homoglyph_flag = "⚠️ Homoglyph Detected" if homoglyph else "✔️ Normal"
    st.markdown(
        f"""
        <div style="background-color: #000000; color: #ffffff; padding: 15px; 
                    border-radius: 10px; font-size: 18px; font-weight: bold; 
                    text-align: center; margin-top: 10px;">
            🕵️‍♂️ Homoglyph Check: {homoglyph_flag}
        </div>
        """,
        unsafe_allow_html=True
    )
