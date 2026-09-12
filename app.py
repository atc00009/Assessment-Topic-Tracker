import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="Assessment Topic Tracker", page_icon="🎯", layout="centered")

# Custom Styling (Vibrant Dark Card Theme with High Visibility)
st.markdown("""
    <style>
    /* Background Page Styling */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    }
    
    /* Header Styling */
    .main-title {
        color: #38bdf8;
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 0 2px 10px rgba(56, 189, 248, 0.3);
    }
    .sub-title {
        color: #cbd5e1;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* Form Container Styling */
    [data-testid="stForm"] {
        background: #1e293b;
        border-radius: 20px;
        padding: 35px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
        border: 2px solid #3b82f6;
    }
    
    /* Form Labels & Text - Extra Large & High Contrast */
    [data-testid="stForm"] label {
        color: #f8fafc !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
    }
    
    /* Dropdown and Input Boxes Text Colors */
    .stTextInput input, div[data-baseweb="select"] {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
    }
    
    /* Submit Button - Vibrant Gradient */
    div.stButton > button {
        background: linear-gradient(90deg, #ec4899 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        border: none !important;
        width: 100%;
        margin-top: 15px;
        box-shadow: 0 4px 20px rgba(236, 72, 153, 0.4);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(236, 72, 153, 0.6);
    }
    
    /* Section Headers */
    .section-header {
        color: #38bdf8;
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 35px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Main Titles
st.markdown('<p class="main-title">🎯 Assessment Topic Tracker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Arden University • Register & Track Your Assessment Topic</p>', unsafe_allow_html=True)

# Shared Data Storage
if "submissions" not in st.session_state:
    st.session_state.submissions = pd.DataFrame(columns=["Student Email", "Chosen Question", "Progress Status"])

# Master Student Validation List
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

# Registration Form Card
with st.form("tracker_form"):
    user_email_input = st.text_input(
        "1. Enter Your Arden Student ID or Email:", 
        placeholder="e.g., 26102538"
    ).strip().lower()
    
    selected_question = st.selectbox("2. Which Assessment Question Are You Working On?", QUESTION_OPTIONS)
    selected_status = st.selectbox("3. What Is Your Current Progress Stage?", STATUS_OPTIONS)
    
    submitted = st.form_submit_button("🚀 Submit Selection")

# Form Validation & Processing
if submitted:
    formatted_email = user_email_input if "@" in user_email_input else f"{user_email_input}@ardenuniversity.ac.uk"
    
    if not user_email_input:
        st.error("⚠️ Please enter your Student ID or Email.")
    elif formatted_email not in [e.lower() for e in VALID_STUDENTS]:
        st.error("❌ Student ID not recognized. Please check your student ID number.")
    elif selected_question == QUESTION_OPTIONS[0]:
        st.error("⚠️ Please select an assessment question from the list.")
    else:
        df = st.session_state.submissions
        df = df[df["Student Email"].str.lower() != formatted_email]
        
        new_entry = pd.DataFrame([{
            "Student Email": formatted_email,
            "Chosen Question": selected_question,
            "Progress Status": selected_status
        }])
        
        st.session_state.submissions = pd.concat([df, new_entry], ignore_index=True)
        
        st.success(f"✅ Selection logged for student: **{formatted_email}**")
        st.info(f"**Topic:** {selected_question}\n\n**Status:** {selected_status}")

# Anonymized Class Summary Section
st.markdown('<h3 class="section-header">📊 Class Topic Overview</h3>', unsafe_allow_html=True)

if st.session_state.submissions.empty:
    st.info("No submissions logged yet. Be the first to register your topic!")
else:
    topic_counts = st.session_state.submissions["Chosen Question"].value_counts().reset_index()
    topic_counts.columns = ["Question / Topic", "Total Students Selected"]
    st.dataframe(topic_counts, use_container_width=True, hide_index=True)
