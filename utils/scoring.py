import pandas as pd
import joblib

# Load trained model and encoders
model = joblib.load("models/risk_model.pkl")
encoders = joblib.load("models/label_encoders.pkl")

def predict_risk(df):
    df_encoded = df.copy()
    categorical_cols = ['Business_Type', 'Existing_Loan', 'Location', 'Owner_Education']

    # Encode using trained encoders
    for col in categorical_cols:
        if col in df.columns:
            df_encoded[col] = encoders[col].transform(df[col])

    # Prepare features
    features = df_encoded.drop(['Business_ID'], axis=1)
    predictions = model.predict(features)
    probabilities = model.predict_proba(features)[:, 1]  # Prob of default

    # Return results
    df['Risk_Prediction'] = predictions
    df['Risk_Probability (%)'] = (probabilities * 100).round(2)
    return df
