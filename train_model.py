import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
import os

# 1. Load your dataset
df = pd.read_csv("data/msme_loan_dataset.csv")

# 2. Drop missing rows (if any)
df.dropna(inplace=True)

# 3. Encode text columns to numbers
categorical_cols = ['Business_Type', 'Existing_Loan', 'Location', 'Owner_Education']
encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le  # Save encoders

# 4. Split into input (X) and output (y)
X = df.drop(['Business_ID', 'Risk_Flag'], axis=1)
y = df['Risk_Flag']

# 5. Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# 7. Print model results
y_pred = model.predict(X_test)
print("📊 Classification Report:")
print(classification_report(y_test, y_pred))

# 8. Save model and encoders
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/risk_model.pkl")
joblib.dump(encoders, "models/label_encoders.pkl")

print("\n✅ Model and encoders saved in 'models/' folder.")
