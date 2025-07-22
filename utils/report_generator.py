from fpdf import FPDF
import os
from datetime import datetime

def generate_pdf_report(results_df, filename="msme_risk_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "MSME Loan Risk Assessment Report", ln=True, align="C")

    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(50, 10, "Business Name", 1)
    pdf.cell(40, 10, "Loan Amount", 1)
    pdf.cell(40, 10, "Risk", 1)
    pdf.cell(30, 10, "Score", 1)
    pdf.ln()

    pdf.set_font("Arial", '', 12)
    for idx, row in results_df.head(20).iterrows():
        pdf.cell(50, 10, str(row['Business_Name'])[:15], 1)
        pdf.cell(40, 10, str(row['LoanAmount']), 1)
        pdf.cell(40, 10, str(row['Risk_Prediction']), 1)
        pdf.cell(30, 10, str(row['Risk_Score']), 1)
        pdf.ln()

    os.makedirs("reports", exist_ok=True)
    report_path = os.path.join("reports", filename)
    pdf.output(report_path)
    return report_path
