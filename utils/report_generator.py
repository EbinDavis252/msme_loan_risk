from fpdf import FPDF
from datetime import datetime
import os

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'MSME Loan Risk Assessment Report', ln=1, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def generate_pdf_report(result_df, chart_path, save_path):
    risk_counts = result_df['Predicted_Risk'].value_counts()

    pdf = PDFReport()
    pdf.add_page()

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    pdf.cell(0, 10, f"Total Records: {len(result_df)}", ln=True)
    pdf.cell(0, 10, f"High Risk: {risk_counts.get('High Risk', 0)}", ln=True)
    pdf.cell(0, 10, f"Low Risk: {risk_counts.get('Low Risk', 0)}", ln=True)

    pdf.cell(0, 10, "", ln=True)
    if os.path.exists(chart_path):
        pdf.image(chart_path, x=60, y=None, w=90)

    pdf.output(save_path)
