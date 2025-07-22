import streamlit as st
import pandas as pd
import sqlite3
import os
from utils.auth import create_user_table, add_user, login_user
from utils.database import create_upload_table, log_upload, fetch_uploads

create_user_table()
create_upload_table()

if "username" not in st.session_state:
    st.session_state.username = None

st.sidebar.title("🔐 Login / Signup")

# LOGIN
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
    filename = uploaded_file.name
    # Save file
    filepath = os.path.join("data/uploaded_data", filename)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.read())

    # 🔐 Log upload
    if st.session_state.username:
        log_upload(st.session_state.username, filename)

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
from utils.visualizations import (
    pie_chart_risk_distribution,
    bar_chart_by_business_type,
    boxplot_loan_risk,
    histogram_risk_prob,
    heatmap_correlation,
    countplot_location
)

if 'results_df' in locals() or 'results_df' in globals():
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

# Show sample
st.subheader("📂 Preview of Built-in Dataset")
sample = pd.read_csv("data/msme_loan_dataset.csv")
st.dataframe(sample.head())

conn.close()
from utils.report_generator import generate_pdf_report

# Section: PDF REPORT
st.subheader("📄 Generate Risk Report")

if 'results_df' in locals() and results_df is not None:
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

    # Simulated Email Alert
    st.subheader("📧 Simulated Email Alert")
    high_risk_count = (results_df['Risk_Prediction'] == 'High Risk').sum()
    total = len(results_df)
    st.info(f"""
    📤 Sending alert to loan officer...
    - High Risk MSMEs: {high_risk_count}/{total}
    - Urgent Review Recommended for flagged businesses.
    """)
else:
    st.warning("⚠️ Please upload a dataset and run the risk prediction first to generate a report.")
# Section: Simulated Email Alert
st.subheader("📧 Simulated Email Alert")
high_risk_count = (results_df['Risk_Prediction'] == 'High Risk').sum()
total = len(results_df)

st.info(f"""
📤 Sending alert to loan officer...
- High Risk MSMEs: {high_risk_count}/{total}
- Urgent Review Recommended for flagged businesses.
""")
if st.session_state.role == "admin":
    st.subheader("🛠 Admin Panel: Upload Tracker")
    data = fetch_uploads()
    if data:
        df_uploads = pd.DataFrame(data, columns=["ID", "Username", "File", "Time"])
        with st.expander("📋 View Upload History"):
            st.dataframe(df_uploads)
    else:
        st.info("No uploads found.")
