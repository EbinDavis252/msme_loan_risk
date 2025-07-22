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

# Setup
st.set_page_config(page_title="MSME Loan Risk Assessment", layout="wide")
st.title("📊 AI-Powered MSME Loan Risk & Credit Assessment System")

# Create Folders
os.makedirs("database", exist_ok=True)
os.makedirs("data/uploaded_data", exist_ok=True)

# Initialize Tables
create_user_table()
create_upload_table()

# User Session Initialization
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = None

# Sidebar Login/Signup
st.sidebar.title("🔐 User Access")

if not st.session_state.username:
    login_tab, signup_tab = st.sidebar.tabs(["🔑 Login", "📝 Sign Up"])

    with login_tab:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.username = user[0]
                st.session_state.role = user[2]
                st.success(f"✅ Welcome {user[0]}!")
                st.rerun()
            else:
                st.error("❌ Incorrect username or password.")

    with signup_tab:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Create Account"):
            add_user(new_user, new_pass)
            st.success("✅ Account created! You can now log in.")
else:
    st.sidebar.success(f"🟢 Logged in as: {st.session_state.username}")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()

# ----------------------------
# 📁 Upload File Section
# ----------------------------
st.sidebar.header("📂 Upload MSME Loan CSV File")
uploaded_file = st.sidebar.file_uploader("Upload MSME Loan Application Data", type=["csv"])

if uploaded_file:
    filename = uploaded_file.name
    if not filename.endswith(".csv"):
        st.sidebar.error("❌ Please upload a valid CSV file.")
    elif uploaded_file.size > 5 * 1024 * 1024:
        st.sidebar.error("⚠️ File too large. Max limit is 5MB.")
    else:
        filepath = os.path.join("data/uploaded_data", filename)
        with open(filepath, "wb") as f:
            f.write(uploaded_file.read())

        try:
            df = pd.read_csv(filepath)
            with sqlite3.connect("data/msme_risk.db") as conn:
                df.to_sql("loan_applications", conn, if_exists="replace", index=False)

            st.success(f"✅ File '{filename}' uploaded and saved successfully!")

            if st.session_state.username:
                log_upload(st.session_state.username, filename)

            st.subheader("📄 Uploaded Data Preview")
            st.dataframe(df.head())

            if st.button("🤖 Predict Loan Default Risk"):
                try:
                    results_df = predict_risk(df)
                    st.session_state["results_df"] = results_df

                    with sqlite3.connect("data/msme_risk.db") as conn:
                        results_df.to_sql("loan_applications", conn, if_exists="replace", index=False)

                    st.success("✅ Prediction completed and stored in DB!")

                    st.subheader("🔍 Risk Prediction Results")
                    st.dataframe(results_df)
                except Exception as e:
                    st.error(f"Prediction error: {e}")
        except Exception as e:
            st.error(f"❌ File processing error: {e}")

# ----------------------------
# 📊 Risk Analysis Dashboard
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
    # 📄 Generate PDF Report
    # ----------------------------
    st.subheader("📄 Generate Risk Report")
    if st.button("Generate PDF Report"):
        try:
            pdf_path = generate_pdf_report(results_df)
            with open(pdf_path, "rb") as f:
                st.success("✅ PDF report generated!")
                st.download_button(
                    label="📥 Download Report",
                    data=f,
                    file_name="msme_loan_risk_report.pdf",
                    mime="application/octet-stream"
                )
        except Exception as e:
            st.error(f"❌ PDF generation failed: {e}")

    # ----------------------------
    # 📧 Simulated Email Alert
    # ----------------------------
    st.subheader("📧 Simulated Email Alert")
    high_risk_count = (results_df['Risk_Prediction'] == 'High Risk').sum()
    total = len(results_df)
    st.info(f"""
    📤 Simulating email alert to loan officers...
    - ⚠️ High Risk MSMEs: {high_risk_count}/{total}
    - Immediate Review Recommended.
    """)

# ----------------------------
# 🛠 Admin Panel
# ----------------------------
if st.session_state.username and st.session_state.role == "admin":
    st.subheader("🛠 Admin Panel: Upload Tracker")
    try:
        data = fetch_uploads()
        if data:
            df_uploads = pd.DataFrame(data, columns=["ID", "Username", "File", "Timestamp"])
            with st.expander("📋 View Upload History"):
                st.dataframe(df_uploads)
        else:
            st.info("No uploads found.")
    except Exception as e:
        st.error(f"Error loading admin panel: {e}")
