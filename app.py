import streamlit as st
import pandas as pd
import sqlite3
import os
from utils.auth import create_user_table, add_user, login_user
from utils.database import create_upload_table, log_upload, fetch_uploads
from utils.scoring import predict_risk
from utils.report_generator import generate_pdf_report
from utils.visualizations import (
    pie_chart_risk_distribution,
    bar_chart_by_business_type,
    boxplot_loan_risk,
    histogram_risk_prob,
    heatmap_correlation,
    countplot_location
)

# Initial Setup
create_user_table()
create_upload_table()

# Streamlit Page Setup
st.set_page_config(page_title="MSME Loan Risk Assessment", layout="wide")
st.title("📊 AI-Powered MSME Loan Risk & Credit Assessment System")

if "username" not in st.session_state:
    st.session_state.username = None

st.sidebar.title("🔐 Login / Signup")

# LOGIN or SIGNUP Interface
if st.session_state.username is None:
    login_tab, signup_tab = st.sidebar.tabs(["🔑 Login", "📝 Sign Up"])

    with login_tab:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.username = user[0]
                st.session_state.role = user[2]
                st.success(f"Welcome {user[0]}!")
                st.rerun()
            else:
                st.error("Incorrect username or password.")

    with signup_tab:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Create Account"):
            add_user(new_user, new_pass)
            st.success("Account created! You can now log in.")
else:
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.username = None
        st.rerun()

# Upload File Section
st.sidebar.header("📁 Upload MSME Loan Application Data")
uploaded_file = st.sidebar.file_uploader("Upload your MSME Loan CSV", type=["csv"])

# Create folders
os.makedirs("database", exist_ok=True)
os.makedirs("data/uploaded_data", exist_ok=True)

if uploaded_file is not None:
    filename = uploaded_file.name
    filepath = os.path.join("data/uploaded_data", filename)

    # Save uploaded file
    with open(filepath, "wb") as f:
        f.write(uploaded_file.read())

    df = pd.read_csv(filepath)

    # Save uploaded data to SQLite
    try:
        with sqlite3.connect("data/msme_risk.db") as conn:
            df.to_sql("loan_applications", conn, if_exists="replace", index=False)
        st.success(f"✅ File '{filename}' uploaded and saved to DB successfully!")
    except Exception as e:
        st.error(f"Database save error: {e}")

    # Log upload
    if st.session_state.username:
        log_upload(st.session_state.username, filename)

    # Show Data Preview
    st.subheader("📄 Uploaded Data Preview")
    st.dataframe(df.head())

    # Predict Risk
    if st.button("🤖 Predict Loan Default Risk"):
        try:
            results_df = predict_risk(df)
            st.session_state["results_df"] = results_df

            st.subheader("🔍 Risk Prediction Results")
            st.dataframe(results_df)

            # Save predictions
            with sqlite3.connect("data/msme_risk.db") as conn:
                results_df.to_sql("loan_applications", conn, if_exists="replace", index=False)
            st.success("✅ Predictions stored in database!")
        except Exception as e:
            st.error(f"Prediction error: {e}")

# ----------------------------
# RISK ANALYSIS DASHBOARD
# ----------------------------
if "results_df" in st.session_state:
    results_df = st.session_state["results_df"]
    st.subheader("📈 Risk Analysis Dashboard")

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(pie_chart_risk_distribution(results_df))
    with col2:
        st.pyplot(bar_chart_by_business_type(results_df))

    st.pyplot(boxplot_loan_risk(results_df))
    st.pyplot(histogram_risk_prob(results_df))
    st.pyplot(heatmap_correlation(results_df))
    st.pyplot(countplot_location(results_df))

    # ----------------------------
    # PDF REPORT
    # ----------------------------
    st.subheader("📄 Generate Risk Report")
    if st.button("Generate PDF Report"):
        pdf_path = generate_pdf_report(results_df)
        with open(pdf_path, "rb") as f:
            st.success("✅ PDF report generated successfully.")
            st.download_button(
                label="📥 Download Report",
                data=f,
                file_name="msme_loan_risk_report.pdf",
                mime="application/octet-stream"
            )

    # ----------------------------
    # SIMULATED EMAIL ALERT
    # ----------------------------
    st.subheader("📧 Simulated Email Alert")
    high_risk_count = (results_df['Risk_Prediction'] == 'High Risk').sum()
    total = len(results_df)
    st.info(f"""
    📤 Sending alert to loan officer...
    - High Risk MSMEs: {high_risk_count}/{total}
    - Urgent Review Recommended for flagged businesses.
    """)

# ----------------------------
# ADMIN PANEL
# ----------------------------
if st.session_state.username and st.session_state.get("role") == "admin":
    st.subheader("🛠 Admin Panel: Upload Tracker")
    data = fetch_uploads()
    if data:
        df_uploads = pd.DataFrame(data, columns=["ID", "Username", "File", "Time"])
        with st.expander("📋 View Upload History"):
            st.dataframe(df_uploads)
    else:
        st.info("No uploads found.")
