import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="Assessment Topic Tracker", page_icon="📝", layout="centered")

# Custom Bright Theme CSS
st.markdown("""
    <style>
    /* Force Bright White Background */
    .stApp {
        background-color: #ffffff !important;
    }
    
    /* Main Title - Dark Yellow / Gold & Extra Large */
    .main-title {
        color: #b45309 !important;
        font-family: 'Arial', sans-serif;
        font-size: 2.8rem !important;
        font-weight: 900 !important;
        text-align: center;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #d97706 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 25px;
    }
    
    /* Clean Card Container on White Background */
    [data-testid="stForm"] {
        background-color: #fefce8 !important; /* Soft warm yellow card */
        border: 3px solid #f59e0b !important;
        border-radius: 16px !important;
        padding: 30px !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08) !important;
    }
    
    /* Form Labels - Large Dark Yellow Text */
    [data-testid="stForm"] label {
        color: #b45309 !important;
        font-size: 1.35rem !important;
        font-weight: 800 !important;
    }
    
    /* Input Text Boxes & Dropdowns Font Size */
    .stTextInput input, div[data-baseweb="select"] {
        font-size: 1.15rem !important;
        color: #1f2937 !important;
    }
    
    /* Submit Button - Vibrant Green */
    div.stButton > button {
        background-color: #16a34a !important;
        color: #ffffff !important;
        font-size: 1.4rem !important;
        font-weight: 900 !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        border: none !important;
        width: 100% !important;
        margin-top: 15px !important;
        box-shadow: 0 4px 12px rgba(22, 163, 74, 0.3) !important;
    }
    div.stButton > button:hover {
        background-color: #15803d !important;
        cursor: pointer;
    }
    
    /* Section Headers */
    .section-header {
        color: #b45309 !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Main Titles
st.markdown('<p class="main-title">📝 Assessment Topic Tracker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Arden University • Register & Track Your Topic Choice</p>', unsafe_allow_html=True)

# Shared Data Storage
if "submissions" not in st.session_state:
    st.session_state.submissions = pd.DataFrame(columns=["Student Email", "Chosen Question", "Progress Status"])

# Master Roster
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

# Bright Yellow Form Card
with st.form("tracker_form"):
    user_email_input = st.text_input(
        "1. Enter Your Arden Student ID or Email:", 
        placeholder="e.g., 26102538"
    ).strip().lower()
    
    selected_question = st.selectbox("2. Which Assessment Question Are You Working On?", QUESTION_OPTIONS)
    selected_status = st.selectbox("3. What Is Your Current Progress Stage?", STATUS_OPTIONS)
    
    submitted = st.form_submit_button(" Submit Selection")

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
        
        st.success(f" Selection logged for student: **{formatted_email}**")
        st.info(f"**Topic:** {selected_question}\n\n**Status:** {selected_status}")

# Anonymized Class Summary Section
st.markdown('<p class="section-header">📊 Class Topic Overview</p>', unsafe_allow_html=True)

if st.session_state.submissions.empty:
    st.info("No submissions logged yet.")
else:
    topic_counts = st.session_state.submissions["Chosen Question"].value_counts().reset_index()
    topic_counts.columns = ["Question / Topic", "Total Students Selected"]
    st.dataframe(topic_counts, use_container_width=True, hide_index=True)
