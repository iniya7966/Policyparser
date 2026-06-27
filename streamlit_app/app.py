import os
import streamlit as st

def load_css():
    """Loads the custom CSS file to apply premium styling."""
    css_path = os.path.join(os.path.dirname(__file__), 'assets', 'style.css')
    try:
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Fallback if the path structure is slightly different
        fallback_path = os.path.join("streamlit_app", "assets", "style.css")
        if os.path.exists(fallback_path):
            with open(fallback_path, "r") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def init_session_state():
    """Initializes standard session state keys for the application."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.uploaded_file = None
        st.session_state.uploaded_file_name = None
        st.session_state.analysis_results = None
        st.session_state.current_page = "Home"
        
        # Populate history with realistic mock data
        st.session_state.history = [
            {
                "id": "POL-9842",
                "name": "Standard_Property_Policy.pdf",
                "date": "2026-06-25 14:32",
                "type": "Property Insurance",
                "prediction": "Approved / Low Risk",
                "confidence": 94.2,
                "risk_score": 18,
                "clauses_count": 8,
                "summary": "This policy provides comprehensive coverage for the insured commercial property. It includes fire, windstorm, and water damage coverages with standard exclusions. The liability limits are adequate, and no high-risk clauses were detected in the primary sections.",
                "clauses": [
                    {"section": "Section 4.1 - Coverage Limits", "text": "Liability limit capped at $2,000,000 per occurrence.", "risk": "Low"},
                    {"section": "Section 9.3 - Deductibles", "text": "Standard deductible of $5,000 applies to all windstorm claims.", "risk": "Low"},
                    {"section": "Section 12.2 - Exclusion Clause", "text": "Excludes mold damage unless directly caused by fire.", "risk": "Medium"}
                ]
            },
            {
                "id": "POL-7210",
                "name": "Cyber_Liability_Policy.pdf",
                "date": "2026-06-22 09:15",
                "type": "Cyber Insurance",
                "prediction": "Needs Review / High Risk",
                "confidence": 88.5,
                "risk_score": 75,
                "clauses_count": 14,
                "summary": "This policy covers cyber breach response, business interruption, and liability. Critical risks identified include a highly restrictive data backup mandate and a tight 24-hour incident notification window, which may invalidate claims if not strictly followed.",
                "clauses": [
                    {"section": "Section 3.2 - Notification Period", "text": "Insured must notify the insurer within 24 hours of detecting any potential breach.", "risk": "High"},
                    {"section": "Section 7.1 - Encryption Requirement", "text": "All data must be encrypted in transit and at rest using AES-256 or policy is void.", "risk": "High"},
                    {"section": "Section 15.4 - Subrogation Waiver", "text": "Waives right to subrogate against third-party software vendors.", "risk": "Medium"}
                ]
            },
            {
                "id": "POL-5541",
                "name": "Executive_Health_Group_Policy.pdf",
                "date": "2026-06-18 16:45",
                "type": "Group Health Insurance",
                "prediction": "Approved / Low Risk",
                "confidence": 97.8,
                "risk_score": 12,
                "clauses_count": 5,
                "summary": "Standard group health benefits package. Standard coverages apply with clear definition of pre-existing conditions and co-payment tiers. Overall risk profile is low and within standard industry boundaries.",
                "clauses": [
                    {"section": "Section 2.3 - Pre-existing Conditions", "text": "No waiting period for pre-existing conditions under group coverage.", "risk": "Low"},
                    {"section": "Section 5.1 - Out-of-pocket Maximum", "text": "Individual out-of-pocket maximum limited to $3,500 annually.", "risk": "Low"}
                ]
            }
        ]

def sidebar_navigation():
    """Renders the custom sidebar header and navigations."""
    with st.sidebar:
        # Custom logo and title using CSS classes
        st.markdown(
"""<div class="sidebar-header">
<div class="sidebar-logo">PP</div>
<div class="sidebar-title">PolicyParser</div>
</div>""", 
            unsafe_allow_html=True
        )
        
        st.markdown("<p style='font-size: 0.85rem; color: #cbd5e1; margin-bottom: 20px; font-weight: 500;'>AI-Powered Insurance Policy Analysis</p>", unsafe_allow_html=True)
        st.write("---")

# Main page configuration
st.set_page_config(
    page_title="PolicyParser - AI Insurance Policy Platform",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load global styling
load_css()

# Initialize session state
init_session_state()

# Render standard sidebar branding
sidebar_navigation()

# Auto-redirect execution to the Home page if app.py is accessed directly
if __name__ == "__main__":
    st.switch_page("pages/1_Home.py")
