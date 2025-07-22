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

# Ensure folders
os.makedirs("database", exist_ok=True)
os.makedirs("data/uploaded_data", exist_ok=True)

# Setup
create_user_table()
create_upload_table()
st.set_page_config(page_title="MSME IntelliRisk Pro", layout="wide")

# Inject CSS for background and sidebar
st.markdown("""
    <style>
        /* Color-changing background animation */
        body {
            animation: bg-change 20s infinite;
            background-size: 400% 400%;
        }
        @keyframes bg-change {
            0% {background-color: #e0f7fa;}
            25% {background-color: #e1bee7;}
            50% {background-color: #ffecb3;}
            75% {background-color: #c8e6c9;}
            100% {background-color: #e0f7fa;}
        }

        /* Sidebar constant color */
        .css-1d391kg, .css-1fv8s86, .css-hxt7ib {
            background-color: #263238 !important;
            color: white;
        }

        h1 {
            font-family: 'Trebuchet MS', sans-serif;
            color: #2e7d32;
            text-align: center;
            font-size: 48px;
        }
    </style>
""", unsafe_allow_html=True)

# Stylish Title
st.markdown("<h1>🤖 MSME IntelliRisk Pro</h1>", unsafe_allow_html=True)

# Session state init
if "username" not in st.session_state:
    st.session_state.username = None
if "registered" not in st.session_state:
    st.session_state.registered = False

# Sidebar Login/Signup
st.sidebar.title("🔐 User Access")

if st.session_state.username is None:
    if not st.session_state.registered:
        st.sidebar.subheader("📝 Register First")
        new_user = st.sidebar.text_input("Create Username")
        new_pass = st.sidebar.text_input("Create Password", type="password")
        if st.sidebar.button("Register"):
            if new_user and new_pass:
                add_user(new_user, new_pass)
                st.success("✅ Registered! You may now login.")
                st.session_state.registered = True
            else:
                st.error("Please enter both username and password.")
    else:
        st.sidebar.subheader("🔑 Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.username = user[0]
                st.session_state.role = user[2]
                st.success(f"Welcome {user[0]}!")
                st.rerun()
            else:
                st.error("Invalid credentials.")
else:
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.username = None
        st.session_state.registered = False
        st.rerun()

# Upload Section
st.sidebar.header("📁 Upload MSME Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

# Dashboard Button
dashboard = st.sidebar.button("📊 View Dashboard")

# Main Body
if uploaded_file is not None:
    filename = uploaded_file.name
    filepath = os.path.join("data/uploaded_data", filename)

    with open(filepath, "wb") as f:
        f.write(uploaded_file.read())

    df = pd.read_csv(filepath)
    st.session_state["raw_data"] = df

    with sqlite3.connect("data/msme_risk.db") as conn:
        df.to_sql("loan_applications", conn, if_exists="replace", index=False)

    if st.session_state.username:
        log_upload(st.session_state.username, filename)

    st.success(f"✅ File '{filename}' uploaded and stored!")

    st.subheader("📄 Uploaded Data Preview")
    st.dataframe(df.head())

    if st.button("🤖 Predict Risk"):
        try:
            results_df = predict_risk(df)
            st.session_state["results_df"] = results_df

            with sqlite3.connect("data/msme_risk.db") as conn:
                results_df.to_sql("loan_applications", conn, if_exists="replace", index=False)

            st.success("✅ Prediction Completed!")
            st.subheader("🔍 Prediction Results")
            st.dataframe(results_df)
        except Exception as e:
            st.error(f"Prediction Error: {e}")

# Show Dashboard
if dashboard and "results_df" in st.session_state:
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

    # PDF
    st.subheader("📄 Generate Risk Report")
    if st.button("📥 Download PDF Report"):
        pdf_path = generate_pdf_report(results_df)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download PDF", data=f, file_name="msme_risk_report.pdf")

    # Email Simulation
    st.subheader("📧 Email Alert")
    high_risk = (results_df['Risk_Prediction'] == 'High Risk').sum()
    total = len(results_df)
    st.info(f"⚠️ Email Sent: {high_risk}/{total} MSMEs are high risk!")

# Admin Panel
if st.session_state.username and st.session_state.get("role") == "admin":
    st.subheader("🛠 Admin Panel: Upload Logs")
    data = fetch_uploads()
    if data:
        df_uploads = pd.DataFrame(data, columns=["ID", "Username", "File", "Time"])
        with st.expander("📂 View Upload History"):
            st.dataframe(df_uploads)
    else:
        st.info("No uploads found.")
