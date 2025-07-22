import streamlit as st
import pandas as pd
import os
from utils.scoring import predict_risk
from utils.visualizations import donut_chart_risk
import base64

# Set page config
st.set_page_config(page_title="MSME Loan Risk & Credit Assessment", layout="wide")

# Title
st.title("💼 MSME Loan Risk & Credit Assessment System")
st.markdown("This AI-powered tool predicts MSME loan default risk and generates credit insights.")

# Upload section
st.sidebar.header("📤 Upload MSME Dataset")
uploaded_file = st.sidebar.file_uploader("Upload your MSME CSV file", type=["csv"])

# Load dataset
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")

        st.subheader("📄 Uploaded Data Preview")
        st.dataframe(df.head())

        # Remove target column if present to avoid prediction errors
        if 'Risk_Flag' in df.columns:
            df = df.drop(columns=['Risk_Flag'])

        # Predict risk
        results_df = predict_risk(df)

        st.subheader("🔍 Prediction Results")
        st.dataframe(results_df)

        # Downloadable CSV
        csv = results_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        st.markdown(f'<a href="data:file/csv;base64,{b64}" download="loan_risk_predictions.csv" class="button">📥 Download Results CSV</a>', unsafe_allow_html=True)

        # Donut chart visualization
        st.subheader("📊 Risk Distribution Overview")
        fig1 = donut_chart_risk(results_df)
        st.pyplot(fig1)

    except Exception as e:
        st.error(f"❌ Error reading or processing the file: {e}")
else:
    st.info("Please upload a valid CSV file to proc
