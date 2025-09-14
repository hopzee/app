import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from extract_features import extract_features

# Load the dataset
df = pd.read_csv("verified_urls.csv").dropna()

# Extract features
X = df["url"].apply(extract_features).apply(pd.Series)
y = df["label"]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, "phishing_model.pkl")
print("✅ Model trained and saved as phishing_model.pkl")
