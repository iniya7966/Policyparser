import streamlit as st
import os
import sys

# Add the parent directory to Python's system path to import modules from app.py
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from app import load_css, init_session_state, sidebar_navigation

# Configure the page
st.set_page_config(
    page_title="PolicyParser - AI Analysis",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load global styling
load_css()
init_session_state()
sidebar_navigation()

st.markdown("<h1>📊 AI Policy Analysis</h1>", unsafe_allow_html=True)

# Helper function to render a colored risk badge
def get_risk_badge(risk_level):
    if risk_level.lower() == "high":
        return '<span class="badge badge-danger">High Risk</span>'
    elif risk_level.lower() == "medium":
        return '<span class="badge badge-warning">Medium Risk</span>'
    else:
        return '<span class="badge badge-success">Low Risk</span>'

# Case 1: No analysis results available
if st.session_state.analysis_results is None:
    st.warning("⚠️ No active policy analysis found.")
    st.markdown("<p style='color:#cbd5e1;'>Please upload a policy PDF document first or load a completed audit from history.</p>", unsafe_allow_html=True)
    
    col_up, col_hist = st.columns(2)
    with col_up:
        if st.button("Go to Upload Page", use_container_width=True):
            st.switch_page("pages/2_Upload.py")
            
    with col_hist:
        if st.button("Go to History Dashboard", use_container_width=True):
            st.switch_page("pages/5_History.py")
            
    # Allow loading a policy directly from history for testing/demo convenience
    st.write("---")
    st.markdown("### Load Sample History Audit")
    
    for record in st.session_state.history:
        col_rec_name, col_rec_type, col_rec_action = st.columns([3, 2, 1])
        with col_rec_name:
            st.write(f"📄 **{record['name']}**")
        with col_rec_type:
            st.write(record['type'])
        with col_rec_action:
            if st.button("Load Audit", key=f"load_{record['id']}"):
                st.session_state.analysis_results = record
                st.session_state.uploaded_file_name = record['name']
                st.rerun()

# Case 2: Active analysis loaded
else:
    res = st.session_state.analysis_results
    
    # Subheader with details
    st.markdown(
f"""<div style="display:flex; justify-content:space-between; margin-bottom: 25px; color:#cbd5e1; border-bottom:1px solid #334155; padding-bottom:10px;">
<span>Document: <b>{res['name']}</b> ({res['type']})</span>
<span>Analyzed On: <b>{res['date']}</b></span>
</div>""",
        unsafe_allow_html=True
    )
    
    # Top Level Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="Risk Assessment", value=res['prediction'].split(" / ")[0], delta=res['prediction'].split(" / ")[1], delta_color="inverse" if "High" in res['prediction'] else "normal")
    with m2:
        st.metric(label="Risk Exposure Score", value=f"{res['risk_score']} / 100", delta="-4" if res['risk_score'] < 30 else "+12", delta_color="inverse")
    with m3:
        st.metric(label="AI Confidence Level", value=f"{res['confidence']}%", delta="High Precision")
    with m4:
        st.metric(label="Critical Clauses Extracted", value=res['clauses_count'])
        
    st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
    
    # Main Dashboard Columns
    col_main, col_sidebar = st.columns([5, 3])
    
    with col_main:
        # AI Executive Summary
        st.markdown(
f"""<div class="premium-card animate-fade-in animate-delay-1 pro-max-hover">
<h3 style="color:#3B82F6; margin-top:0; border-bottom: 1px solid #334155; padding-bottom: 10px;">🧠 AI Executive Summary</h3>
<p style="color:#cbd5e1; line-height:1.7; font-size:1rem; margin-top:15px;">
{res['summary']}
</p>
</div>""",
            unsafe_allow_html=True
        )
        
        # Extracted Important Clauses
        st.markdown("### Extracted Critical Clauses")
        
        for idx, clause in enumerate(res['clauses']):
            badge_html = get_risk_badge(clause['risk'])
            st.markdown(
f"""<div class="clause-box animate-fade-in animate-delay-2">
<div class="clause-header">
<div class="clause-title">{clause['section']}</div>
{badge_html}
</div>
<div style="color:#cbd5e1; font-style:italic; font-size:0.92rem; line-height:1.6; margin-top:5px;">
"{clause['text']}"
</div>
</div>""",
                unsafe_allow_html=True
            )
            
    with col_sidebar:
        # Prediction & Recommendation Card
        badge_class = "badge-success" if "Low" in res['prediction'] else "badge-danger"
        text_color = "#10B981" if "Low" in res['prediction'] else "#EF4444"
        
        st.markdown(
f"""<div class="recommendation-card animate-scale-up animate-delay-2 pro-max-hover">
<h3 style="margin-top:0; color:#FFFFFF;">🛡️ Compliance Decision</h3>
<div style="font-size:1.5rem; font-weight:700; color:{text_color}; margin: 15px 0;">
{res['prediction']}
</div>
<p style="color:#cbd5e1; font-size:0.9rem; line-height:1.6;">
Based on language analysis, this policy is graded at <b>{res['risk_score']}% risk exposure</b>.
</p>
</div>""",
            unsafe_allow_html=True
        )
        
        # AI Insights card
        st.markdown(
"""<div class="premium-card animate-fade-in animate-delay-3">
<h4 style="margin-top:0; color:#F59E0B; border-bottom: 1px solid #334155; padding-bottom: 8px;">💡 Policy Recommendations</h4>
<ul style="color:#cbd5e1; padding-left:20px; line-height:1.7; font-size:0.88rem; margin-top:10px;">
<li>Ensure all standard definitions match state statutes of limitation.</li>
<li>Verify deductibles are in line with enterprise liquidity thresholds.</li>
<li>Check if subrogation waiver limits liability of key vendors.</li>
<li>Add specific riders if external hardware security breach liability is required.</li>
</ul>
</div>""",
            unsafe_allow_html=True
        )
        
        # Navigation to Report
        if st.button("Generate & Export Full Report", use_container_width=True):
            st.switch_page("pages/4_Report.py")
            
        # Re-upload button
        if st.button("Analyze Another Document", use_container_width=True, type="secondary"):
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
