import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="Assessment Topic Tracker", page_icon="📝", layout="centered")

# Main Title & Subtitle
st.title("📝 Assessment Topic Tracker")
st.caption("Arden University • Register & Track Your Assessment Topic")
st.divider()

# Shared Data Storage
if "submissions" not in st.session_state:
    st.session_state.submissions = pd.DataFrame(columns=["Student Email", "Chosen Question", "Progress Status"])

# Master Roster (Hidden from students)
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

# Clean Form Section
with st.container():
    st.subheader("📋 Registration Form")
    
    with st.form("tracker_form"):
        user_email_input = st.text_input(
            "1. Student ID or Email", 
            placeholder="e.g., 26102538 or 26102538@ardenuniversity.ac.uk"
        ).strip().lower()
        
        selected_question = st.selectbox("2. Selected Assessment Question", QUESTION_OPTIONS)
        selected_status = st.selectbox("3. Current Progress Stage", STATUS_OPTIONS)
        
        submitted = st.form_submit_button("Submit Selection", type="primary", use_container_width=True)

# Submission Processing
if submitted:
    formatted_email = user_email_input if "@" in user_email_input else f"{user_email_input}@ardenuniversity.ac.uk"
    
    if not user_email_input:
        st.error("⚠️ Please enter your Student ID or Email.")
    elif formatted_email not in [e.lower() for e in VALID_STUDENTS]:
        st.error("❌ Student ID not recognized. Please check your student ID number.")
    elif selected_question == QUESTION_OPTIONS[0]:
        st.error("⚠️ Please select an assessment question from the dropdown.")
    else:
        # Overwrite previous entry if re-submitted
        df = st.session_state.submissions
        df = df[df["Student Email"].str.lower() != formatted_email]
        
        new_entry = pd.DataFrame([{
            "Student Email": formatted_email,
            "Chosen Question": selected_question,
            "Progress Status": selected_status
        }])
        
        st.session_state.submissions = pd.concat([df, new_entry], ignore_index=True)
        
        st.success(f"✅ Topic selection logged for **{formatted_email}**!")
        st.info(f"**Topic:** {selected_question}\n\n**Status:** {selected_status}")

st.divider()

# Class Overview Section
st.subheader("📊 Class Topic Overview")

if st.session_state.submissions.empty:
    st.info("No selections recorded yet.")
else:
    topic_counts = st.session_state.submissions["Chosen Question"].value_counts().reset_index()
    topic_counts.columns = ["Question / Topic", "Total Students"]
    st.dataframe(topic_counts, use_container_width=True, hide_index=True)
