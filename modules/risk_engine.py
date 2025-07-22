# modules/risk_engine.py

import pandas as pd

def categorize_risk(score):
    if score >= 0.7:
        return "🚨 High Risk"
    elif score >= 0.4:
        return "⚠️ Medium Risk"
    else:
        return "✅ Low Risk"

def generate_recommendation(row):
    if row['risk_level'] == "🚨 High Risk":
        return "Decline or request collateral. Perform on-site verification."
    elif row['risk_level'] == "⚠️ Medium Risk":
        return "Ask for additional documents. Conduct credit bureau review."
    else:
        return "Approve with standard conditions."

def apply_risk_engine(df):
    # Example rule: Higher loan amount + lower income → higher risk score
    df["risk_score"] = (df["loan_amount"] / (df["annual_income"] + 1)).clip(0, 1)
    df["risk_level"] = df["risk_score"].apply(categorize_risk)
    df["recommendation"] = df.apply(generate_recommendation, axis=1)
    return df
