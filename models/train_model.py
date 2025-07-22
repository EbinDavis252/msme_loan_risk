import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
import os

# Load sample data
df = pd.read_csv("data/sample_msmse_data.csv")

# Encode categorical columns
categorical_cols = ['Business_Type', 'Existing_Loan', 'Location', 'Owner_Education']
encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

# Features & Target
X = df.drop(['Business_ID', 'Risk_Flag'], axis=1)
y = df['Risk_Flag']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/risk_model.pkl")
joblib.dump(encoders, "models/label_encoders.pkl")
print("✅ Model and encoders saved!")
