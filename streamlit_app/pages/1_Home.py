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
    page_title="PolicyParser - AI Insurance Policy Platform",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize application settings and load CSS
load_css()
init_session_state()
sidebar_navigation()

# Hero Section
st.markdown(
"""<div class="hero-container">
<div class="hero-title">PolicyParser</div>
<div class="hero-subtitle">
An ultra-modern, AI-powered platform designed to break down, analyze, and demystify complex insurance policies in seconds. Empower your decision-making with automated risk profiling and semantic summaries.
</div>
</div>""",
    unsafe_allow_html=True
)

# Get Started Button (Aligned center)
col_left, col_btn, col_right = st.columns([2, 1, 2])
with col_btn:
    if st.button("Get Started Analyze", use_container_width=True):
        st.switch_page("pages/2_Upload.py")

st.markdown("<div style='margin-bottom: 60px;'></div>", unsafe_allow_html=True)

# Overview Section
st.markdown("## Platform Capabilities")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
"""<div class="premium-card animate-fade-in animate-delay-1 pro-max-hover">
<h3 style="color:#3B82F6; margin-top:0;">🤖 Deep AI Extraction</h3>
<p style="color:#cbd5e1; line-height:1.6; font-size:0.95rem;">
Leverage state-of-the-art NLP models trained specifically on commercial legal documents to extract key coverages, exclusions, limits, and obligations automatically.
</p>
</div>""",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
"""<div class="premium-card animate-fade-in animate-delay-2 pro-max-hover">
<h3 style="color:#10B981; margin-top:0;">⚖️ Risk & Compliance Scoring</h3>
<p style="color:#cbd5e1; line-height:1.6; font-size:0.95rem;">
Instantly identify high-liability terminology, restrictive backup requirements, short breach-notification windows, and hidden indemnity waivers before signing.
</p>
</div>""",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
"""<div class="premium-card animate-fade-in animate-delay-3 pro-max-hover">
<h3 style="color:#F59E0B; margin-top:0;">📋 Structured Reporting</h3>
<p style="color:#cbd5e1; line-height:1.6; font-size:0.95rem;">
Compile comprehensive compliance reviews and risk breakdowns into clean, client-facing PDF documents, ready for distribution to stakeholders and legal teams.
</p>
</div>""",
        unsafe_allow_html=True
    )

st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

# How It Works
st.markdown("## Streamlined Workflow")
st.markdown("---")

step1, step2, step3, step4 = st.columns(4)

with step1:
    st.markdown(
"""<div class="stat-card animate-scale-up animate-delay-1 pro-max-hover">
<div style="font-size:2.5rem; margin-bottom:10px;">📤</div>
<div class="stat-label">Step 1</div>
<h4 style="margin: 10px 0 5px 0;">Upload Policy</h4>
<p style="font-size:0.85rem; color:#cbd5e1; margin:0;">Upload insurance agreement PDFs directly onto the platform.</p>
</div>""",
        unsafe_allow_html=True
    )

with step2:
    st.markdown(
"""<div class="stat-card animate-scale-up animate-delay-2 pro-max-hover">
<div style="font-size:2.5rem; margin-bottom:10px;">⚡</div>
<div class="stat-label">Step 2</div>
<h4 style="margin: 10px 0 5px 0;">AI Parsing</h4>
<p style="font-size:0.85rem; color:#cbd5e1; margin:0;">Our machine learning models extract clauses, conditions and definitions.</p>
</div>""",
        unsafe_allow_html=True
    )

with step3:
    st.markdown(
"""<div class="stat-card animate-scale-up animate-delay-3 pro-max-hover">
<div style="font-size:2.5rem; margin-bottom:10px;">📊</div>
<div class="stat-label">Step 3</div>
<h4 style="margin: 10px 0 5px 0;">Audit & Analyze</h4>
<p style="font-size:0.85rem; color:#cbd5e1; margin:0;">Review risk metrics, severity scoring, and extracted recommendations.</p>
</div>""",
        unsafe_allow_html=True
    )

with step4:
    st.markdown(
"""<div class="stat-card animate-scale-up animate-delay-4 pro-max-hover">
<div style="font-size:2.5rem; margin-bottom:10px;">📥</div>
<div class="stat-label">Step 4</div>
<h4 style="margin: 10px 0 5px 0;">Export & Share</h4>
<p style="font-size:0.85rem; color:#cbd5e1; margin:0;">Download structured PDF analysis, summary reports and key matrices.</p>
</div>""",
        unsafe_allow_html=True
    )

st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)

# Performance Statistics
st.markdown("## Platform Statistics")
st.markdown("---")

stat1, stat2, stat3, stat4 = st.columns(4)

with stat1:
    st.markdown(
"""<div class="stat-card">
<div class="stat-label">Extraction Accuracy</div>
<div class="stat-val">98.4%</div>
<span class="badge badge-success">Top Tier Industry Grade</span>
</div>""",
        unsafe_allow_html=True
    )

with stat2:
    st.markdown(
"""<div class="stat-card">
<div class="stat-label">Analysis Speed</div>
<div class="stat-val">&lt; 15s</div>
<span class="badge badge-info">Near Instantaneous</span>
</div>""",
        unsafe_allow_html=True
    )

with stat3:
    st.markdown(
"""<div class="stat-card">
<div class="stat-label">Active Deployments</div>
<div class="stat-val">25+</div>
<span class="badge badge-info">SaaS Accounts</span>
</div>""",
        unsafe_allow_html=True
    )

with stat4:
    st.markdown(
"""<div class="stat-card">
<div class="stat-label">Policies Processed</div>
<div class="stat-val">12,500+</div>
<span class="badge badge-success">Production Ready</span>
</div>""",
        unsafe_allow_html=True
    )

# Footer
st.markdown(
"""<div class="footer-container">
<p>© 2026 PolicyParser Inc. All rights reserved. Powered by Advanced Machine Learning.</p>
<p style="color:#64748b; font-size:0.75rem;">Developed for Enterprise Risk Assessment and Policy Intelligence.</p>
</div>""",
    unsafe_allow_html=True
)
