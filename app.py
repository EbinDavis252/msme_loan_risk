import streamlit as st
import pandas as pd
import os
from utils.preprocessing import preprocess
from utils.scoring import predict_risk
from utils.visualizations import donut_chart_risk
import matplotlib.pyplot as plt

st.set_page_config(page_title="MSME Loan Risk Assessment", layout="wide")
st.title("🧠 AI-Powered MSME Loan Risk & Credit Assessment System")

# Upload section
st.sidebar.header("📁 Upload MSME Dataset")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read and preprocess
    df = pd.read_csv(uploaded_file)
    st.subheader("📄 Uploaded Data Preview")
    st.dataframe(df.head())

    try:
        processed_df = preprocess(df)
        predictions = predict_risk(processed_df)

        # Combine with original
        results_df = df.copy()
        results_df['Predicted_Risk'] = predictions

        # Show prediction results
        st.subheader("🔍 Risk Prediction Results")
        st.dataframe(results_df[['Predicted_Risk']].value_counts().reset_index(name='Count'))

        # Generate donut chart
        if not results_df.empty:
            fig1 = donut_chart_risk(results_df)

            st.subheader("📊 Risk Distribution (Donut Chart)")
            st.pyplot(fig1)

            # Save the chart
            os.makedirs("charts", exist_ok=True)
            chart_path = os.path.join("charts", "donut_chart.png")
            fig1.savefig(chart_path)
            st.success("📁 Donut chart saved to 'charts/donut_chart.png'")

    except Exception as e:
        st.error(f"❌ Error during prediction: {e}")

else:
    st.info("👈 Upload a CSV file from the sidebar to begin.")
