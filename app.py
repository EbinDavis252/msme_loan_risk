import streamlit as st
import pandas as pd
import sqlite3
import os

# Set up Streamlit page
st.set_page_config(page_title="MSME Loan Risk Assessment", layout="wide")
st.title("📊 AI-Powered MSME Loan Risk & Credit Assessment System")

# Sidebar upload
st.sidebar.header("📁 Upload MSME Loan Application Data")
uploaded_file = st.sidebar.file_uploader("Upload your MSME Loan CSV", type=["csv"])

# Create DB folder
os.makedirs("database", exist_ok=True)

# Create DB and Table
conn = sqlite3.connect("database/msme_applications.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS loan_applications (
    Business_ID TEXT,
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

# Process uploaded file
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.dataframe(df)

    # Save to DB
    if st.button("📥 Save to Database"):
        df.to_sql("loan_applications", conn, if_exists="replace", index=False)
        st.success("🗄️ Data saved to SQLite database!")
    
    # Predict Risk
    from utils.scoring import predict_risk

    if st.button("🤖 Predict Loan Default Risk"):
        try:
            results_df = predict_risk(df)
            st.subheader("🔍 Risk Prediction Results")
            st.dataframe(results_df)

            # Save results back to DB
            results_df.to_sql("loan_applications", conn, if_exists="replace", index=False)
            st.success("✅ Predictions stored in database!")

        except Exception as e:
            st.error(f"Prediction error: {e}")

from utils.visualizations import pie_chart_risk, bar_chart_by_business_type

if 'results_df' in locals():
    st.subheader("📊 Visual Analysis of MSME Risk")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ✅ Safe vs Risky MSMEs")
        fig1 = pie_chart_risk(results_df)
        st.pyplot(fig1)

    with col2:
        st.markdown("### 🏢 Avg Risk % by Business Type")
        fig2 = bar_chart_by_business_type(results_df)
        st.pyplot(fig2)

    # Filterable credit score table
    st.subheader("📋 Credit Scorecard")
    status_filter = st.selectbox("Filter by Risk Prediction", options=["All", "Safe", "Risky"])
    if status_filter == "Safe":
        st.dataframe(results_df[results_df["Risk_Prediction"] == 0])
    elif status_filter == "Risky":
        st.dataframe(results_df[results_df["Risk_Prediction"] == 1])
    else:
        st.dataframe(results_df)

    # Download CSV
    st.subheader("📥 Download Scored Data")
    csv = results_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download as CSV", csv, "msme_risk_scored.csv", "text/csv")

# Show sample
st.subheader("📂 Preview of Built-in Dataset")
sample = pd.read_csv("data/msme_loan_dataset.csv")
st.dataframe(sample.head())

conn.close()
