import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Page Configuration
st.set_page_config(page_title="Assessment Topic Tracker", page_icon="📝", layout="centered")

# Custom Styling
st.markdown("""
    <style>
    /* Force Bright White Page Background */
    .stApp {
        background-color: #ffffff !important;
    }
    
    /* Main Title & Subtitle */
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
    [data-testid="stForm"] label, label, div[data-testid="stWidgetLabel"] p {
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
    }
    
    /* Light Theme Fix on Data Tables */
    div[data-testid="stDataFrame"], 
    div[data-testid="stDataFrame"] * {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
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

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Helper function to read the latest submissions from Google Sheets
def get_submissions():
    try:
        df = conn.read(ttl="0s") # Force reload latest data
        if df.empty or "Student Email" not in df.columns:
            return pd.DataFrame(columns=["Student Email", "Chosen Question", "Progress Status"])
        return df
    except Exception:
        return pd.DataFrame(columns=["Student Email", "Chosen Question", "Progress Status"])

submissions_df = get_submissions()

# Master Roster Validation List
STUDENT_ID_OPTIONS = [
    "-- Select Your Student ID --",
    "25247104",
    "26102538",
    "26104991",
    "26130240",
    "26136522",
    "26143544",
    "STU202542",
    "26102203"
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
    selected_student_id = st.selectbox("1. Select Your Arden Student ID:", STUDENT_ID_OPTIONS, key="input_student_id")
    selected_question = st.selectbox("2. Which Assessment Question Are You Working On?", QUESTION_OPTIONS, key="input_question")
    selected_status = st.selectbox("3. What Is Your Current Progress Stage?", STATUS_OPTIONS, key="input_status")
    
    submitted = st.form_submit_button("Submit Selection")

# Form Processing
if submitted:
    if selected_student_id == STUDENT_ID_OPTIONS[0]:
        st.error("⚠️ Please select your Student ID from the dropdown list.")
    elif selected_question == QUESTION_OPTIONS[0]:
        st.error("⚠️ Please select an assessment question from the list.")
    else:
        formatted_email = f"{selected_student_id.lower()}@ardenuniversity.ac.uk"
        
        # Filter out old record for this student and append new record
        df_updated = submissions_df[submissions_df["Student Email"].str.lower() != formatted_email]
        
        new_entry = pd.DataFrame([{
            "Student Email": formatted_email,
            "Chosen Question": selected_question,
            "Progress Status": selected_status
        }])
        
        df_final = pd.concat([df_updated, new_entry], ignore_index=True)
        
        # Save updated data straight back to Google Sheets
        conn.update(data=df_final)
        st.cache_data.clear() # Clear cache to refresh values instantly
        
        st.success(f"✅ Selection recorded for Student ID: **{selected_student_id}**")
        st.rerun() # Reload page to display updated stats

st.divider()

# Public View: Aggregate Class Statistics Table (GDPR Compliant)
st.markdown('<p class="section-header">📊 Class Topic Statistics</p>', unsafe_allow_html=True)

all_questions = QUESTION_OPTIONS[1:]

if submissions_df.empty:
    default_df = pd.DataFrame({
        "Assessment Question / Topic": all_questions,
        "Total Students Selected": [0] * len(all_questions)
    })
    st.dataframe(default_df, use_container_width=True, hide_index=True)
else:
    counts = submissions_df["Chosen Question"].value_counts()
    summary_data = []
    for q in all_questions:
        summary_data.append({
            "Assessment Question / Topic": q,
            "Total Students Selected": counts.get(q, 0)
        })
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

# SECRET TUTOR ACCESS VIA URL QUERY PARAMETER (?pin=com4025!)
if st.query_params.get("pin") == "com4025!":
    st.divider()
    st.markdown('<p class="section-header">🔒 Tutor Control Panel (Private)</p>', unsafe_allow_html=True)
    
    st.markdown("### 📋 Student Roster Submissions")
    if submissions_df.empty:
        st.info("No student submissions logged yet.")
    else:
        st.dataframe(
            submissions_df[["Student Email", "Chosen Question", "Progress Status"]], 
            use_container_width=True, 
            hide_index=True
        )
    
    st.markdown("### ⚙️ Admin Tools")
    if st.button("🗑️ Clear All Data in Google Sheet"):
        empty_df = pd.DataFrame(columns=["Student Email", "Chosen Question", "Progress Status"])
        conn.update(data=empty_df) # Clears sheet content
        st.cache_data.clear()
        st.success("Google Sheet wiped!")
        st.rerun()
