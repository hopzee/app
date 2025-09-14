import pandas as pd
from extract_features import safe_extract_features
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# ===== Step 1: Load datasets =====
urldata = pd.read_csv("urldata.csv", names=['URL', 'Label'])
urldata1 = pd.read_csv("urldata1.csv", on_bad_lines='skip')  # skip bad lines
urls_data = pd.read_csv("urls_data.txt")  # change sep='\t' if tab-separated

# ===== Step 2: Standardize column names =====
# urldata.csv
urldata['Label'] = urldata['Label'].map({'bad':1, 'good':0})

# urldata1.csv: rename first so cleaning works
urldata1.rename(columns={'url':'URL', 'result':'Label'}, inplace=True)

# urls_data.txt: rename columns
urls_data.rename(columns={'url':'URL', 'label':'Label'}, inplace=True)

# ===== Step 3: Clean URLs =====
# Replace '[.]' with '.' to fix malformed URLs
urldata['URL'] = urldata['URL'].str.replace(r'\[\.\]', '.', regex=True)
urldata1['URL'] = urldata1['URL'].str.replace(r'\[\.\]', '.', regex=True)

# ===== Step 4: Extract features =====
print("Extracting features from urldata.csv ...")
features_urldata = urldata['URL'].apply(safe_extract_features)
features_urldata_df = pd.DataFrame(features_urldata.tolist())
features_urldata_df['Label'] = urldata['Label'].values

print("Extracting features from urldata1.csv ...")
features_urldata1 = urldata1['URL'].apply(safe_extract_features)
features_urldata1_df = pd.DataFrame(features_urldata1.tolist())
features_urldata1_df['Label'] = urldata1['Label'].values

# urls_data already has features, drop URL column
features_urls_data = urls_data.drop(columns=['URL'])

# ===== Step 5: Combine datasets =====
final_dataset = pd.concat([features_urldata_df, features_urldata1_df, features_urls_data], ignore_index=True)

# ===== Step 6: Fill NaN values =====
final_dataset = final_dataset.fillna(0)

# ===== Step 7: Preview =====
print("Combined dataset preview:")
print(final_dataset.head())
print("\nLabel distribution:")
print(final_dataset['Label'].value_counts())

# ===== Step 8: Train Random Forest model =====
X = final_dataset.drop(columns=['Label'])
y = final_dataset['Label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(class_weight='balanced', n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ===== Step 9: Save model =====
joblib.dump(model, "phishing_model.pkl")
print("\n✅ Model trained and saved as phishing_model.pkl")
