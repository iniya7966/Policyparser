import streamlit as st
import os
import sys
import time

# Add the parent directory to Python's system path to import modules from app.py
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from app import load_css, init_session_state, sidebar_navigation

# Configure the page
st.set_page_config(
    page_title="PolicyParser - Upload Policy",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load global styling
load_css()
init_session_state()
sidebar_navigation()

st.markdown("<h1>📤 Document Upload</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#cbd5e1; font-size:1.1rem; margin-bottom:30px;'>Upload your insurance policy PDF for analysis.</p>", unsafe_allow_html=True)

# Layout: 2 columns (Uploader left, Info panel right)
col_upload, col_info = st.columns([3, 2])

with col_upload:
    st.markdown("### Select Policy File")
    
    # Supported policy types dropdown to customize mock results
    policy_type = st.selectbox(
        "Select Insurance Policy Type",
        ["Commercial General Liability", "Cyber Security Liability", "Property & Casualty", "Group Health Insurance", "Professional Indemnity / D&O"]
    )
    
    # Drag & drop upload widget
    uploaded_file = st.file_uploader(
        "Choose an insurance policy PDF file",
        type=["pdf"],
        help="Upload a standard PDF policy contract. Scanning and OCR will be performed automatically if required."
    )
    
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        
        # Format file size
        file_size_kb = len(uploaded_file.getvalue()) / 1024
        file_size_str = f"{file_size_kb:.2f} KB" if file_size_kb < 1024 else f"{file_size_kb/1024:.2f} MB"
        
        st.session_state.uploaded_file_name = uploaded_file.name
        
        # Display File details card
        st.markdown(
f"""<div class="premium-card animate-fade-in animate-delay-1 pro-max-hover">
<h4 style="margin-top:0; color:#3B82F6;">📋 File Metadata</h4>
<table style="width:100%; border-collapse:collapse; color:#cbd5e1; font-size:0.9rem;">
<tr style="border-bottom:1px solid #334155;"><td style="padding:8px 0; font-weight:600; width:40%;">Filename:</td><td style="padding:8px 0;">{uploaded_file.name}</td></tr>
<tr style="border-bottom:1px solid #334155;"><td style="padding:8px 0; font-weight:600;">Size:</td><td style="padding:8px 0;">{file_size_str}</td></tr>
<tr style="border-bottom:1px solid #334155;"><td style="padding:8px 0; font-weight:600;">Type:</td><td style="padding:8px 0;">{policy_type}</td></tr>
</table>
</div>""",
            unsafe_allow_html=True
        )
        
        # Action button to trigger processing animation
        if st.button("Begin AI Policy Analysis", use_container_width=True):
            # Simulation of AI parsing pipeline
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            stages = [
                (10, "📖 Ingesting PDF file and parsing pages..."),
                (30, "🔍 Running OCR and structural block detection..."),
                (50, "🤖 Extracting policy parameters & clauses..."),
                (75, "⚖️ Evaluating liability limits, exclusions, and legal risks..."),
                (90, "📈 Computing confidence score and compiling metrics..."),
                (100, "✅ Document processed successfully!")
            ]
            
            for percent, msg in stages:
                status_text.markdown(f"<p style='color:#3B82F6; font-weight:500;'>{msg}</p>", unsafe_allow_html=True)
                progress_bar.progress(percent)
                time.sleep(0.6)
                
            # Create customized mock analysis result depending on user selection
            if "Cyber" in policy_type:
                pred = "Needs Review / High Risk"
                conf = 89.4
                risk = 78
                summary = "The policy provides general cyber response coverage, but contains an extremely high-risk clause mandating 24-hour incident notification and standard backup systems verification. Missing these metrics can void coverages entirely."
                clauses = [
                    {"section": "Section 2.1 - Data Protection Standards", "text": "The insured must implement and maintain dual-factor authentication on all administrative endpoints.", "risk": "Medium"},
                    {"section": "Section 4.3 - Breach Reporting", "text": "Written notice of any actual or suspected data breach must be delivered to the insurer within 24 hours of discovery.", "risk": "High"},
                    {"section": "Section 9.5 - Backup Obligations", "text": "System logs and backups must be replicated offsite weekly. Failure to verify restoration capabilities monthly voids business interruption liability.", "risk": "High"}
                ]
            elif "Property" in policy_type:
                pred = "Approved / Low Risk"
                conf = 95.0
                risk = 15
                summary = "Standard commercial property risk configuration. Core clauses cover physical damage, business interruption, and liability. Clear deductible and coinsurance structures are listed with normal limits."
                clauses = [
                    {"section": "Section 3.1 - Insured Premises", "text": "Covers physical damage to structures and inventory caused by fire, windstorm, and hail.", "risk": "Low"},
                    {"section": "Section 7.2 - Coinsurance Condition", "text": "Requires insured to maintain coverage equal to at least 80% of actual cash value.", "risk": "Low"},
                    {"section": "Section 11.4 - Excluded Risks", "text": "Excludes damages caused by earthquakes or flood waters unless specific riders are attached.", "risk": "Medium"}
                ]
            else:
                pred = "Approved / Low Risk"
                conf = 91.2
                risk = 28
                summary = "Standard general insurance agreement template. Coverage boundaries and liability maximums are within healthy limits. No major legal or subrogation anomalies detected."
                clauses = [
                    {"section": "Section 1.2 - Premium Payment", "text": "Monthly premium due on the 1st of each calendar month. Grace period of 15 days applies.", "risk": "Low"},
                    {"section": "Section 5.5 - Severability", "text": "If any provision is found invalid, it will not affect the validity of remaining contract parts.", "risk": "Low"},
                    {"section": "Section 8.1 - Dispute Resolution", "text": "Any claim disputes must be settled through binding arbitration in state court.", "risk": "Medium"}
                ]
                
            # Store in session state for Analysis and Report pages
            st.session_state.uploaded_file = uploaded_file
            st.session_state.analysis_results = {
                "id": f"POL-{int(time.time()) % 10000}",
                "name": uploaded_file.name,
                "date": time.strftime("%Y-%m-%d %H:%M"),
                "type": policy_type,
                "prediction": pred,
                "confidence": conf,
                "risk_score": risk,
                "clauses_count": len(clauses),
                "summary": summary,
                "clauses": clauses
            }
            
            # Save into history
            st.session_state.history.insert(0, st.session_state.analysis_results)
            
            # Switch to Analysis page
            st.switch_page("pages/3_Analysis.py")

with col_info:
    st.markdown("### Upload Specifications")
    
    st.markdown(
"""<div class="premium-card animate-fade-in animate-delay-2" style="background: rgba(15, 23, 42, 0.4);">
<h4 style="margin-top:0; color:#3B82F6;">✔️ Supported Guidelines</h4>
<ul style="color:#cbd5e1; padding-left:20px; line-height:1.8; font-size:0.9rem;">
<li>Acceptable files: <b>Adobe PDF (.pdf)</b></li>
<li>Maximum file size: <b>50 MB</b></li>
<li>Standard PDF readable text format</li>
<li>Image/scanned PDFs supported via OCR parser</li>
</ul>
</div>
<div class="premium-card animate-fade-in animate-delay-3" style="background: rgba(15, 23, 42, 0.4);">
<h4 style="margin-top:0; color:#F59E0B;">⚠️ Legal Disclaimer</h4>
<p style="color:#cbd5e1; line-height:1.6; font-size:0.85rem; margin:0;">
PolicyParser provides AI-assisted summaries and risk evaluations for administrative facilitation only. It does not constitute official legal advice or formal underwriting decisions. Always double-check critical terms directly with legal counsel.
</p>
</div>""",
        unsafe_allow_html=True
    )

# Footer
st.markdown(
"""<div class="footer-container">
<p>© 2026 PolicyParser Inc. All rights reserved. Powered by Advanced Machine Learning.</p>
</div>""",
    unsafe_allow_html=True
)
