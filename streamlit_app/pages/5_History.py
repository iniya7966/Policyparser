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
    page_title="PolicyParser - History",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load global styling
load_css()
init_session_state()
sidebar_navigation()

st.markdown("<h1>📜 Policy Audit History</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#cbd5e1; font-size:1.1rem; margin-bottom:30px;'>Manage, search, and reload previous insurance policy audit analyses.</p>", unsafe_allow_html=True)

# Calculation of historical aggregates
total_audits = len(st.session_state.history)
high_risk_count = sum(1 for item in st.session_state.history if "High" in item["prediction"])
avg_risk = int(sum(item["risk_score"] for item in st.session_state.history) / total_audits) if total_audits > 0 else 0
avg_conf = sum(item["confidence"] for item in st.session_state.history) / total_audits if total_audits > 0 else 0.0

# Stats counters Row
s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown(
"""<div class="stat-card animate-scale-up animate-delay-1 pro-max-hover">
<div class="stat-label">Total Audits</div>
<div class="stat-val">{total_audits}</div>
<span class="badge badge-info">All Uploads</span>
</div>""",
        unsafe_allow_html=True
    )
with s2:
    st.markdown(
f"""<div class="stat-card animate-scale-up animate-delay-2 pro-max-hover">
<div class="stat-label">High Risk Profiles</div>
<div class="stat-val" style="color:var(--danger);">{high_risk_count}</div>
<span class="badge badge-danger">Needs Critical Review</span>
</div>""",
        unsafe_allow_html=True
    )
with s3:
    st.markdown(
f"""<div class="stat-card animate-scale-up animate-delay-3 pro-max-hover">
<div class="stat-label">Average Risk Index</div>
<div class="stat-val">{avg_risk} / 100</div>
<span class="badge badge-warning">Moderate Average</span>
</div>""",
        unsafe_allow_html=True
    )
with s4:
    st.markdown(
f"""<div class="stat-card animate-scale-up animate-delay-4 pro-max-hover">
<div class="stat-label">Average Accuracy</div>
<div class="stat-val">{avg_conf:.1f}%</div>
<span class="badge badge-success">High Confidence</span>
</div>""",
        unsafe_allow_html=True
    )

st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

# Search & Filters Section
st.markdown("### Search Audit Records")

col_search, col_filter = st.columns([3, 1])

with col_search:
    search_query = st.text_input("Search policies by file name or ID...", placeholder="e.g. Standard_Property_Policy.pdf")

with col_filter:
    filter_type = st.selectbox(
        "Filter by Policy Category",
        ["All Categories", "Property Insurance", "Cyber Insurance", "Group Health Insurance", "Commercial General Liability", "Professional Indemnity / D&O"]
    )

# Filter processing
filtered_history = []
for record in st.session_state.history:
    # Text Search matches
    search_match = (
        search_query.lower() in record["name"].lower() or 
        search_query.lower() in record["id"].lower() or
        search_query.lower() in record["summary"].lower()
    )
    # Category Filter matches
    category_match = (
        filter_type == "All Categories" or 
        record["type"].lower() == filter_type.lower() or
        (filter_type == "Property Insurance" and "property" in record["type"].lower()) or
        (filter_type == "Cyber Insurance" and "cyber" in record["type"].lower()) or
        (filter_type == "Group Health Insurance" and "health" in record["type"].lower())
    )
    
    if search_match and category_match:
        filtered_history.append(record)

# History Interactive list rows
st.markdown("---")
if not filtered_history:
    st.info("No matching policy audit history records found.")
else:
    # Custom headers
    h_id, h_name, h_type, h_pred, h_risk, h_action = st.columns([1.5, 3, 2, 2.5, 1.5, 1.5])
    with h_id:
        st.markdown("**Audit ID**")
    with h_name:
        st.markdown("**File Name**")
    with h_type:
        st.markdown("**Category**")
    with h_pred:
        st.markdown("**Status Decision**")
    with h_risk:
        st.markdown("**Risk Score**")
    with h_action:
        st.markdown("**Audits**")
        
    st.markdown("<hr style='margin: 8px 0 15px 0; border: none; border-bottom: 1px solid var(--border);'/>", unsafe_allow_html=True)
    
    for idx, item in enumerate(filtered_history):
        # Color coding metrics
        is_high = "High" in item["prediction"]
        pred_color = "#EF4444" if is_high else "#10B981"
        badge_style = "badge-danger" if is_high else "badge-success"
        
        row_id, row_name, row_type, row_pred, row_risk, row_action = st.columns([1.5, 3, 2, 2.5, 1.5, 1.5])
        
        with row_id:
            st.markdown(f"<code style='color:#3B82F6; font-size:0.9rem; font-weight:600;'>{item['id']}</code>", unsafe_allow_html=True)
        with row_name:
            st.markdown(f"<span style='color:#FFFFFF; font-weight:500; font-size:0.95rem;'>{item['name']}</span>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:0.75rem; color:#cbd5e1; margin:0;'>Uploaded: {item['date']}</p>", unsafe_allow_html=True)
        with row_type:
            st.markdown(f"<span style='color:#cbd5e1; font-size:0.9rem;'>{item['type']}</span>", unsafe_allow_html=True)
        with row_pred:
            st.markdown(f"<span class='badge {badge_style}'>{item['prediction'].split(' / ')[0]}</span>", unsafe_allow_html=True)
        with row_risk:
            st.markdown(f"<span style='color:{pred_color}; font-weight:700; font-size:1.05rem;'>{item['risk_score']} / 100</span>", unsafe_allow_html=True)
        with row_action:
            if st.button("Load", key=f"hist_{item['id']}", use_container_width=True):
                st.session_state.analysis_results = item
                st.session_state.uploaded_file_name = item['name']
                st.switch_page("pages/3_Analysis.py")
                
        st.markdown("<hr style='margin: 10px 0; border: none; border-bottom: 1px dashed #334155;'/>", unsafe_allow_html=True)

# Footer
st.markdown(
"""<div class="footer-container">
<p>© 2026 PolicyParser Inc. All rights reserved. Powered by Advanced Machine Learning.</p>
</div>""",
    unsafe_allow_html=True
)
