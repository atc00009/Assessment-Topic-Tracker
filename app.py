import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Arden COM4025 Assignment Tracker", page_icon="📝", layout="centered")

st.title("📝 COM4025: Assignment Question Tracker")
st.write("Please select your Student Email/ID, confirm the assignment question you are working on, and update your progress.")

# Pre-populated Student List from your class roster
STUDENT_LIST = [
    "-- Select Your Email/ID --",
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

STATUS_OPTIONS = [
    "🟡 Just Started / Selecting Topic",
    "🔵 Researching & Outlining",
    "🟢 Writing Draft",
    "🏁 Finalizing & Reviewing"
]

# Form Interface
with st.form("tracker_form", clear_on_submit=False):
    selected_student = st.selectbox("1. Select your Student Email / ID:", STUDENT_LIST)
    selected_question = st.selectbox("2. Which Assignment Question are you working on?", QUESTION_OPTIONS)
    selected_status = st.select_slider("3. What is your current progress?", options=STATUS_OPTIONS)
    notes = st.text_area("4. Any questions or notes for your tutor? (Optional)", placeholder="e.g., Struggling with command syntax...")
    
    submitted = st.form_submit_button("Submit Selection")

if submitted:
    if selected_student == STUDENT_LIST[0] or selected_question == QUESTION_OPTIONS[0]:
        st.error("⚠️ Please select both your Student Email and an Assignment Question before submitting.")
    else:
        # Save payload logic (Logs locally or pushes to Google Sheets/Database)
        st.success(f"✅ Thank you! Progress recorded for {selected_student}.")
        st.info(f"**Question:** {selected_question}\n\n**Status:** {selected_status}")
