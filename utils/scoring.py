import pandas as pd
import joblib

# Load trained model and encoders
model = joblib.load("models/risk_model.pkl")
encoders = joblib.load("models/label_encoders.pkl")

def predict_risk(df):
    df_encoded = df.copy()
    
    # Drop Risk_Flag if present
    if 'Risk_Flag' in df_encoded.columns:
        df_encoded = df_encoded.drop(columns=['Risk_Flag'])

    # Encode categorical features
    categorical_cols = ['Business_Type', 'Existing_Loan', 'Location', 'Owner_Education']
    for col in categorical_cols:
        if col in df_encoded.columns:
            df_encoded[col] = encoders[col].transform(df_encoded[col])

    # Drop Business_ID
    features = df_encoded.drop(['Business_ID'], axis=1)

    # Predict
    predictions = model.predict(features)
    probabilities = model.predict_proba(features)[:, 1]

    # Append results
    df['Risk_Prediction'] = predictions
    df['Risk_Probability (%)'] = (probabilities * 100).round(2)
    return df
