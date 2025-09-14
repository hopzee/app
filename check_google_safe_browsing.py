import streamlit as st
import requests

def is_unsafe_google(url: str) -> bool:
    """
    Check a URL against Google Safe Browsing API.
    Reads API key from .streamlit/secrets.toml file.
    """
    try:
        api_key = st.secrets["google"]["api_key"]  # 🔑 from secrets.toml
    except Exception as e:
        print("⚠️ Google API key not found in .streamlit/secrets.toml")
        return False

    endpoint = "https://safebrowsing.googleapis.com/v4/threatMatches:find"

    payload = {
        "client": {
            "clientId": "phishing-detector",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }

    try:
        response = requests.post(f"{endpoint}?key={api_key}", json=payload, timeout=10)
        result = response.json()
        return bool(result.get("matches"))
    except Exception as e:
        print(f"⚠️ Google Safe Browsing check failed: {e}")
        return False
