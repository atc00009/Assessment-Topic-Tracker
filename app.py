import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="Assessment Topic Tracker", page_icon="🎯", layout="centered")

# Custom Styling (High-Contrast Theme)
st.markdown("""
    <style>
    /* Main Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header Styling */
    .main-title {
        color: #0d253f;
        font-family: 'Helvetica Neue', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #334e68;
        font-size: 1rem;
        text-align: center;
        margin-bottom: 25px;
    }
    
    /* Form Container Styling */
    [data-testid="stForm"] {
        background: #0f172a; /* Deep Navy Card */
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        border: 1px solid #1e293b;
    }
    
    /* Input Labels - High Contrast White Text */
    [data-testid="stForm"] label {
        color: #f8fafc !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
    }
    
    /* Submit Button Custom Color */
    div.stButton > button {
        background: linear-gradient(90deg, #0284c7 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        border: none !important;
        width: 100%;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    div.stButton > button:hover {
        background: linear-gradient(90deg, #0369a1 0%, #1d4ed8 100%) !important;
    }
    
    /* Section Dividers & Table Headers */
    .section-header {
        color: #0f172a;
        font-weight: 700;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<p class="main-title">🎯 Assessment Topic Tracker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Arden University • Enter your details to confirm your topic choice</p>', unsafe_allow_html=True)

# Shared Data Storage
if "submissions" not in st.session_state:
    st.session_state.submissions = pd.DataFrame(columns=["Student Email", "Chosen Question", "Progress Status"])

# Roster Validation List
VALID_STUDENTS = [
    "25247104@ardenuniversity.ac.uk",
    "26102538@ardenuniversity.ac.uk",
    "26104991@ardenuniversity.ac.uk",
    "26130240@ardenuniversity.ac.uk",
    "26136522@ardenuniversity.ac.uk",
    "26143544@ardenuniversity.ac.uk",
    "STU202542@ardenuniversity.ac.uk",
    "26102203@ardenuniversity.ac.uk"
]

QUESTION_OPTIONS = [
    "-- Select Question --",
    "Question 1: Windows OS & Security Policies",
    "Question 2: Principle of Least Privilege & User Access",
    "Question 3: Cyber-Physical Systems & Data Integrity",
    "Undecided / Need Guidance"
]

STATUS_OPTIONS = ["🟡 Topic Selected", "🔵 Researching & Outlining", "🟢 Writing Draft", "🏁 Finalized"]

# Registration Card Form
with st.form("tracker_form"):
    user_email_input = st.text_input(
        "1. Enter your Arden Student ID or Email:", 
        placeholder="e.g., 26102538"
    ).strip().lower()
    
    selected_question = st.selectbox("2. Which Assessment Question are you working on?", QUESTION_OPTIONS)
    selected_status = st.selectbox("3. What is your current progress stage?", STATUS_OPTIONS)
    
    submitted = st.form_submit_button("🚀 Submit Selection")

if submitted:
    formatted_email = user_email_input if "@" in user_email_input else f"{user_email_input}@ardenuniversity.ac.uk"
    
    if not user_email_input:
        st.error("⚠️ Please type your Student ID or Email.")
    elif formatted_email not in [e.lower() for e in VALID_STUDENTS]:
        st.error("❌ Student ID not recognized. Please re-check your student ID number.")
    elif selected_question == QUESTION_OPTIONS[0]:
        st.error("⚠️ Please select an assessment question from the list.")
    else:
        # Overwrite previous entry if student updates choice
        df = st.session_state.submissions
        df = df[df["Student Email"].str.lower() != formatted_email]
        
        new_entry = pd.DataFrame([{
            "Student Email": formatted_email,
            "Chosen Question": selected_question,
            "Progress Status": selected_status
        }])
        
        st.session_state.submissions = pd.concat([df, new_entry], ignore_index=True)
        
        # Confirmation Alert
        st.success(f"✅ Selection logged for student: {formatted_email}")
        st.info(f"**Topic:** {selected_question}\n\n**Status:** {selected_status}")

# Public Anonymized Summary
st.markdown('<h3 class="section-header">📊 Live Class Topic Overview</h3>', unsafe_allow_html=True)

if st.session_state.submissions.empty:
    st.info("No submissions logged yet. Be the first to register your topic!")
else:
    # Summary Table with Custom Colors
    topic_counts = st.session_state.submissions["Chosen Question"].value_counts().reset_index()
    topic_counts.columns = ["Question / Topic", "Total Students Selected"]
    st.dataframe(topic_counts, use_container_width=True, hide_index=True)
