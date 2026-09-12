import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="Assessment Topic Tracker", page_icon="📝", layout="centered")

# Custom Styling (Bright Theme with Compact Fonts & Ash-Grey Inputs)
st.markdown("""
    <style>
    /* Force Bright White Page Background */
    .stApp {
        background-color: #ffffff !important;
    }
    
    /* Main Title & Subtitle - Compact Font Sizes */
    .main-title {
        color: #b45309 !important;
        font-family: 'Arial', sans-serif;
        font-size: 2.0rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 2px;
    }
    .sub-title {
        color: #d97706 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        text-align: center;
        margin-bottom: 18px;
    }
    
    /* Outer Form Card Container */
    [data-testid="stForm"] {
        background-color: #fefce8 !important;
        border: 2px solid #f59e0b !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }
    
    /* Form Labels */
    [data-testid="stForm"] label {
        color: #b45309 !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
    }
    
    /* Light Ash Grey Input Boxes & Dropdowns */
    .stTextInput input, 
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] * {
        background-color: #e2e8f0 !important;
        color: #0f172a !important;
        border-radius: 6px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }

    /* Input Placeholder Text */
    .stTextInput input::placeholder {
        color: #64748b !important;
        font-size: 0.9rem !important;
    }

    /* Dropdown Option Menu Items */
    div[data-baseweb="menu"], div[data-baseweb="menu"] * {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
        font-size: 0.95rem !important;
    }
    
    /* Submit Button - Vibrant Green */
    div.stButton > button {
        background-color: #16a34a !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        border: none !important;
        width: 100% !important;
        margin-top: 10px !important;
        box-shadow: 0 2px 8px rgba(22, 163, 74, 0.2) !important;
    }
    div.stButton > button:hover {
        background-color: #15803d !important;
        cursor: pointer;
    }
    
    /* Section Headers */
    .section-header {
        color: #b45309 !important;
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        margin-top: 22px;
    }
    </style>
""", unsafe_allow_html=True)

# Main Titles
st.markdown('<p class="main-title">📝 Assessment Topic Tracker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Arden University • Register & Track Your Topic Choice</p>', unsafe_allow_html=True)

# Shared Data Storage Setup
if "submissions" not in st.session_state:
    st.session_state.submissions = pd.DataFrame(columns=["Student Email", "Chosen Question", "Progress Status"])

# Master Roster Validation
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
    
    submitted = st.form_submit_button("Submit Selection")

# Form Processing
if submitted:
    formatted_email = user_email_input if "@" in user_email_input else f"{user_email_input}@ardenuniversity.ac.uk"
    
    if not user_email_input:
        st.error("⚠️ Please enter your Student ID or Email.")
    elif formatted_email not in [e.lower() for e in VALID_STUDENTS]:
        st.error("❌ Student ID not recognized. Please check your student ID number.")
    elif selected_question == QUESTION_OPTIONS[0]:
        st.error("⚠️ Please select an assessment question from the list.")
    else:
        # Overwrite previous submission if student re-submits
        df = st.session_state.submissions
        df = df[df["Student Email"].str.lower() != formatted_email]
        
        new_entry = pd.DataFrame([{
            "Student Email": formatted_email,
            "Chosen Question": selected_question,
            "Progress Status": selected_status
        }])
        
        st.session_state.submissions = pd.concat([df, new_entry], ignore_index=True)
        st.success(f"✅ Selection logged for student: **{formatted_email}**")

st.divider()

# Private View: Show the active student their own saved entry
if 'user_email_input' in locals() and user_email_input:
    check_email = user_email_input if "@" in user_email_input else f"{user_email_input}@ardenuniversity.ac.uk"
    user_record = st.session_state.submissions[st.session_state.submissions["Student Email"].str.lower() == check_email]
    
    if not user_record.empty:
        st.markdown('<p class="section-header">👤 Your Saved Selection</p>', unsafe_allow_html=True)
        my_topic = user_record.iloc[0]["Chosen Question"]
        my_status = user_record.iloc[0]["Progress Status"]
        st.info(f"**Student ID:** {check_email}\n\n**Selected Question:** {my_topic}\n\n**Status:** {my_status}")

# Public View: Always-Visible Class Statistics (Anonymized Aggregate View)
st.markdown('<p class="section-header">📊 Class Topic Statistics</p>', unsafe_allow_html=True)

all_questions = QUESTION_OPTIONS[1:] # All valid questions

if st.session_state.submissions.empty:
    default_df = pd.DataFrame({
        "Assessment Question / Topic": all_questions,
        "Total Students Selected": [0] * len(all_questions)
    })
    st.dataframe(default_df, use_container_width=True, hide_index=True)
else:
    counts = st.session_state.submissions["Chosen Question"].value_counts()
    summary_data = []
    for q in all_questions:
        summary_data.append({
            "Assessment Question / Topic": q,
            "Total Students Selected": counts.get(q, 0)
        })
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

# Admin Reset Tool for Testing
with st.expander("⚙️ Admin Testing Tools"):
    if st.button("🗑️ Clear Test Data"):
        st.session_state.submissions = pd.DataFrame(columns=["Student Email", "Chosen Question", "Progress Status"])
        st.rerun()
