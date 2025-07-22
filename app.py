import streamlit as st
import pandas as pd
import sqlite3
import os

# Title
st.set_page_config(page_title="MSME Loan Risk Assessment", layout="wide")
st.title("📊 AI-Powered MSME Loan Risk & Credit Assessment System")

# Upload Section
st.sidebar.header("📁 Upload MSME Loan Application Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

from utils.scoring import predict_risk

# Risk Prediction
if uploaded_file and st.button("🤖 Predict Risk & Score"):
    scored_df = predict_risk(df)
    st.subheader("📊 Prediction Results")
    st.dataframe(scored_df)

    # Save predictions to DB
    scored_df.to_sql("loan_applications", conn, if_exists='replace', index=False)
    st.success("✅ Predictions saved to database!")


# SQLite Database Setup
db_path = "database/msme_applications.db"
os.makedirs("database", exist_ok=True)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS loan_applications (
    Business_ID TEXT PRIMARY KEY,
    Business_Type TEXT,
    Years_in_Business INTEGER,
    Annual_Turnover REAL,
    Existing_Loan TEXT,
    Loan_Amount_Requested REAL,
    Credit_History_Score INTEGER,
    Location TEXT,
    Owner_Education TEXT,
    Risk_Flag INTEGER
)
""")
conn.commit()

# Preview Uploaded Data
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.dataframe(df)

    # Save to database
    if st.button("📥 Save to Database"):
        df.to_sql("loan_applications", conn, if_exists='replace', index=False)
        st.success("🗄️ Data saved to database!")

# Load & Preview Sample
st.subheader("🔍 Sample Dataset Preview")
sample_df = pd.read_csv("data/sample_msmse_data.csv")
st.dataframe(sample_df.head())

# Close DB
conn.close()
