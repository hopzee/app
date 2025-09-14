import pandas as pd
import joblib
from extract_features import extract_features

# Load trained model
model = joblib.load("phishing_model.pkl")

# List of test URLs
test_urls = [
    "https://www.google.com",
    "https://g00gle.com",
    "https://facebook.com",
    "https://faceb00k-login.com",
    "https://accessbankplc.com",
    "https://acc3ssbankplc.com",
    "https://unilag.edu.ng",
    "https://un1lag.edu.ng",
    "https://gtbank.com",
    "https://gtb4nk-login.com"
]

# Loop through test URLs
for url in test_urls:
    features = extract_features(url)
    X = pd.DataFrame([features])
    prediction = model.predict(X)[0]

    print(f"\n🔍 Checking: {url}")
    if prediction == 1:
        print("🚨 Phishing suspected!")
        if features.get("has_homoglyph") == 1:
            print("⚠️ Homoglyph detected in domain.")
    else:
        print("✅ Appears safe.")
