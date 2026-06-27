import streamlit as st
import os
import sys
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# Add the parent directory to Python's system path to import modules from app.py
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from app import load_css, init_session_state, sidebar_navigation

# Configure the page
st.set_page_config(
    page_title="PolicyParser - Export Report",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load global styling
load_css()
init_session_state()
sidebar_navigation()

st.markdown("<h1>📄 Audit Report</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#cbd5e1; font-size:1.1rem; margin-bottom:30px;'>Review, print, and export your completed policy analysis report.</p>", unsafe_allow_html=True)

# Helper function to generate printable report string
def generate_text_report(res):
    report = f"""========================================================================
POLICYPARSER - AI INSURANCE POLICY ANALYSIS REPORT
========================================================================
Audit Reference ID : {res['id']}
Document Name      : {res['name']}
Analysis Timestamp : {res['date']}
Policy Category    : {res['type']}
------------------------------------------------------------------------

1. EXECUTIVE SUMMARY
---------------------
{res['summary']}

------------------------------------------------------------------------
2. RISK PROFILE & DECISION SUMMARY
-----------------------------------
Overall Decision   : {res['prediction']}
Risk Score (0-100) : {res['risk_score']} / 100
AI Confidence      : {res['confidence']}%

------------------------------------------------------------------------
3. CRITICAL CLAUSES AUDIT
--------------------------
"""
    for idx, clause in enumerate(res['clauses'], 1):
        report += f"\n[{idx}] SECTION: {clause['section']}\n"
        report += f"    Severity Level: {clause['risk'].upper()} RISK\n"
        report += f"    Text Extract  : \"{clause['text']}\"\n"
        report += "    ----------------------------------------------------\n"
        
    report += """
------------------------------------------------------------------------
4. COMPLIANCE RECOMMENDATIONS
------------------------------
* Confirm compliance with statutory laws of the respective jurisdiction.
* Address and negotiate high-risk clauses with the underwriting team prior to signing.
* Set up internal tracking for critical breach-reporting/notification deadlines.
* Ensure data encryption guidelines strictly align with company technology capability.

========================================================================
Report compiled automatically by PolicyParser platform.
========================================================================
"""
    return report

def generate_pdf_report(res):
    """Generates a proper PDF document in memory using reportlab."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], alignment=TA_CENTER, fontSize=16, spaceAfter=20)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=12, spaceBefore=15, spaceAfter=10, textColor="#1F2937")
    normal_style = styles['Normal']
    normal_style.spaceAfter = 8
    
    story = []
    
    # Title & Header
    story.append(Paragraph("POLICYPARSER - AI INSURANCE POLICY ANALYSIS REPORT", title_style))
    story.append(Paragraph(f"<b>Audit Reference ID:</b> {res['id']}", normal_style))
    story.append(Paragraph(f"<b>Document Name:</b> {res['name']}", normal_style))
    story.append(Paragraph(f"<b>Analysis Timestamp:</b> {res['date']}", normal_style))
    story.append(Paragraph(f"<b>Policy Category:</b> {res['type']}", normal_style))
    story.append(Spacer(1, 10))
    
    # Section 1
    story.append(Paragraph("1. EXECUTIVE SUMMARY", heading_style))
    story.append(Paragraph(res['summary'], normal_style))
    story.append(Spacer(1, 10))
    
    # Section 2
    story.append(Paragraph("2. RISK PROFILE & DECISION SUMMARY", heading_style))
    story.append(Paragraph(f"<b>Overall Decision:</b> {res['prediction']}", normal_style))
    story.append(Paragraph(f"<b>Risk Score (0-100):</b> {res['risk_score']} / 100", normal_style))
    story.append(Paragraph(f"<b>AI Confidence:</b> {res['confidence']}%", normal_style))
    story.append(Spacer(1, 10))
    
    # Section 3
    story.append(Paragraph("3. CRITICAL CLAUSES AUDIT", heading_style))
    for idx, clause in enumerate(res['clauses'], 1):
        story.append(Paragraph(f"<b>[{idx}] SECTION: {clause['section']}</b>", normal_style))
        story.append(Paragraph(f"<b>Severity Level:</b> {clause['risk'].upper()} RISK", normal_style))
        story.append(Paragraph(f"<b>Text Extract:</b> \"{clause['text']}\"", normal_style))
        story.append(Spacer(1, 5))
        
    # Section 4
    story.append(Paragraph("4. COMPLIANCE RECOMMENDATIONS", heading_style))
    recommendations = [
        "Confirm compliance with statutory laws of the respective jurisdiction.",
        "Address and negotiate high-risk clauses with the underwriting team prior to signing.",
        "Set up internal tracking for critical breach-reporting/notification deadlines.",
        "Ensure data encryption guidelines strictly align with company technology capability."
    ]
    for rec in recommendations:
        story.append(Paragraph(f"• {rec}", normal_style))
        
    story.append(Spacer(1, 20))
    story.append(Paragraph("<i>Report compiled automatically by PolicyParser platform.</i>", ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER)))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# Case 1: No analysis results available
if st.session_state.analysis_results is None:
    st.warning("⚠️ No active policy analysis found.")
    st.markdown("<p style='color:#cbd5e1;'>Please upload a policy PDF document first to generate a report.</p>", unsafe_allow_html=True)
    if st.button("Go to Upload Page", use_container_width=True):
        st.switch_page("pages/2_Upload.py")

# Case 2: Active analysis loaded
else:
    res = st.session_state.analysis_results
    
    # Document header details
    st.markdown(
f"""<div style="background:rgba(17, 24, 39, 0.5); padding:20px; border-radius:12px; border:1px solid #334155; margin-bottom:30px;">
<div style="display:flex; justify-content:space-between; align-items:center;">
<div>
<h3 style="margin:0; color:#3B82F6;">{res['name']}</h3>
<span style="color:#cbd5e1; font-size:0.9rem;">Audit Reference: <b>{res['id']}</b></span>
</div>
<div style="text-align:right;">
<span style="color:#cbd5e1; font-size:0.9rem;">Date Evaluated: {res['date']}</span><br/>
<span class="badge badge-info">{res['type']}</span>
</div>
</div>
</div>""",
        unsafe_allow_html=True
    )
    
    # Generate download report string
    report_text = generate_text_report(res)
    
    col_left, col_right = st.columns([5, 2])
    
    with col_left:
        # Report Card 1: Executive Summary
        st.markdown(
f"""<div class="premium-card animate-fade-in animate-delay-1 pro-max-hover">
<h3 style="color:#FFFFFF; margin-top:0; border-bottom:1px solid #334155; padding-bottom:8px;">1. Executive Summary</h3>
<p style="color:#cbd5e1; line-height:1.7; font-size:0.95rem; margin-top:15px;">
{res['summary']}
</p>
</div>""",
            unsafe_allow_html=True
        )
        
        # Report Card 2: Risk Matrix Table
        st.markdown("### 2. Extracted Clauses Summary")
        
        # Assemble custom HTML table
        table_rows = ""
        for idx, clause in enumerate(res['clauses'], 1):
            if clause['risk'].lower() == "high":
                color_span = '<span style="color:#EF4444; font-weight:600;">HIGH</span>'
            elif clause['risk'].lower() == "medium":
                color_span = '<span style="color:#F59E0B; font-weight:600;">MEDIUM</span>'
            else:
                color_span = '<span style="color:#10B981; font-weight:600;">LOW</span>'
                
            table_rows += f"""<tr>
<td style="font-weight:600; color:#FFFFFF;">{clause['section']}</td>
<td style="font-style:italic;">"{clause['text']}"</td>
<td style="text-align:center;">{color_span}</td>
</tr>"""
            
        st.markdown(
f"""<table class="custom-table">
<thead>
<tr>
<th style="width:30%;">Section Name</th>
<th style="width:55%;">Clause Extract</th>
<th style="width:15%; text-align:center;">Risk Rating</th>
</tr>
</thead>
<tbody>
{table_rows}
</tbody>
</table>""",
            unsafe_allow_html=True
        )
        
    with col_right:
        # Report Card 3: Audit Parameters Info
        st.markdown(
f"""<div class="premium-card animate-fade-in animate-delay-2 pro-max-hover" style="background: rgba(15, 23, 42, 0.4);">
<h4 style="margin-top:0; color:#FFFFFF; border-bottom:1px solid #334155; padding-bottom:8px;">📊 Evaluation Metrics</h4>
<div style="margin:15px 0;">
<div style="font-size:0.8rem; color:#cbd5e1; text-transform:uppercase;">Overall Classification</div>
<div style="font-size:1.25rem; font-weight:700; color:#3B82F6; margin-bottom:10px;">{res['prediction'].split(" / ")[0]}</div>
<div style="font-size:0.8rem; color:#cbd5e1; text-transform:uppercase;">Risk Severity Index</div>
<div style="font-size:1.25rem; font-weight:700; color:{'#EF4444' if res['risk_score'] > 50 else '#10B981'}; margin-bottom:10px;">{res['risk_score']} / 100</div>
<div style="font-size:0.8rem; color:#cbd5e1; text-transform:uppercase;">Parser Confidence</div>
<div style="font-size:1.25rem; font-weight:700; color:#FFFFFF;">{res['confidence']}%</div>
</div>
</div>""",
            unsafe_allow_html=True
        )
        
        # Download panel
        st.markdown("### Export Actions")
        
        # Built-in Streamlit download button
        st.download_button(
            label="Download Text Report (.txt)",
            data=report_text,
            file_name=f"PolicyParser_Report_{res['id']}.txt",
            mime="text/plain",
            use_container_width=True
        )
        
        # Simulate PDF compilation triggering
        if st.button("Generate Official PDF Report", use_container_width=True):
            with st.spinner("Compiling print-ready PDF layout..."):
                # Generate actual PDF file data
                pdf_data = generate_pdf_report(res)
                
            st.success("PDF Compiled successfully! Click below to download.")
            
            # Offer download for the compiled markdown/text styled report as PDF layout preview
            st.download_button(
                label="Click here to download PDF",
                data=pdf_data,
                file_name=f"PolicyParser_Report_{res['id']}.pdf",
                mime="application/pdf",
                key="pdf_download",
                use_container_width=True
            )
            
        if st.button("Analyze New Policy", use_container_width=True, type="secondary"):
            st.session_state.uploaded_file = None
            st.session_state.analysis_results = None
            st.switch_page("pages/2_Upload.py")

# Footer
st.markdown(
"""<div class="footer-container">
<p>© 2026 PolicyParser Inc. All rights reserved. Powered by Advanced Machine Learning.</p>
</div>""",
    unsafe_allow_html=True
)
