import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Assessment Topic Tracker", page_icon="📝", layout="centered")

# Global Light Theme Override (Forces clean white page & light ash inputs)
st.markdown("""
    <style>
    /* Force White Background */
    .stApp, div[data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
    }
    
    /* Title Styles */
    .main-title {
        color: #b45309 !important;
        font-family: 'Arial', sans-serif;
        font-size: 2.6rem !important;
        font-weight: 900 !important;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #d97706 !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 25px;
    }
    
    /* Main Card Box */
    [data-testid="stForm"] {
        background-color: #fefce8 !important;
        border: 3px solid #f59e0b !important;
        border-radius: 16px !important;
        padding: 30px !important;
    }
    
    /* Input Labels */
    [data-testid="stForm"] label p {
        color: #b45309 !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
    }
    
    /* LIGHT ASH GREY INPUT BOXES & DROPDOWNS */
    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background-color: #e2e8f0 !important; /* Ash Grey */
        border: 2px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }
    
    /* Text Inside Inputs and Dropdowns */
    input, div[data-baseweb="select"] * {
        color: #0f172a !important; /* Dark Text */
        font-size: 1.15rem !important;
        font-weight: 700 !important;
    }
    
    /* VIBRANT GREEN SUBMIT BUTTON */
    div[data-testid="stForm"] button {
        background-color: #16a34a !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px !important;
        width: 100% !important;
        margin-top: 15px !important;
    }
    div[data-testid="stForm"] button p {
        color: #ffffff !important;
        font-size: 1.4rem !important;
        font-weight: 900 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Page Header
st.markdown('<p class="main-title">📝 Assessment Topic Tracker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Arden University • Register & Track Your Assessment Topic</p>', unsafe_allow_html=True)

# Data Storage Setup
if "submissions" not in st.session_state:
    st.session_state.submissions = pd.DataFrame(columns=["Student ID / Email", "Chosen Question", "Progress Status"])

# Master Student Roster
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

# Registration Form
with st.form("tracker_form"):
    user_id_input = st.text_input(
        "1. Enter Your Arden Student ID:", 
        placeholder="e.g., 26102538"
    ).strip().lower()
    
    selected_question = st.selectbox("2. Which Assessment Question Are You Working On?", QUESTION_OPTIONS)
    selected_status = st.selectbox("3. What Is Your Current Progress Stage?", STATUS_OPTIONS)
    
    submitted = st.form_submit_button("Submit Selection")

# Form Validation
if submitted:
    formatted_email = user_id_input if "@" in user_id_input else f"{user_id_input}@ardenuniversity.ac.uk"
    
    if not user_id_input:
        st.error("⚠️ Please enter your Student ID.")
    elif formatted_email not in [e.lower() for e in VALID_STUDENTS]:
        st.error("❌ Student ID not recognized. Please check your student ID number.")
    elif selected_question == QUESTION_OPTIONS[0]:
        st.error("⚠️ Please select an assessment question.")
    else:
        # Save / Update entry
        df = st.session_state.submissions
        df = df[df["Student ID / Email"].str.lower() != formatted_email]
        
        new_entry = pd.DataFrame([{
            "Student ID / Email": formatted_email,
            "Chosen Question": selected_question,
            "Progress Status": selected_status
        }])
        
        st.session_state.submissions = pd.concat([df, new_entry], ignore_index=True)
        st.success(f"✅ Topic selection recorded for Student ID: **{user_id_input}**!")

# Anonymized Class Summary Section
st.divider()
st.subheader("📊 Class Topic Overview")

if st.session_state.submissions.empty:
    st.info("No submissions logged yet.")
else:
    topic_counts = st.session_state.submissions["Chosen Question"].value_counts().reset_index()
    topic_counts.columns = ["Question / Topic", "Total Students Selected"]
    st.dataframe(topic_counts, use_container_width=True, hide_index=True)
