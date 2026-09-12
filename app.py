import streamlit as st
import pandas as pd

st.set_page_config(page_title="Assessment Topic Tracker", page_icon="📝", layout="centered")

st.title("📝 Assessment Topic Tracker")
st.write("Select your email and log your assessment question. Your email remains private.")

# Initialize shared data storage
if "submissions" not in st.session_state:
    st.session_state.submissions = pd.DataFrame(columns=["Student Email", "Chosen Question", "Progress Status"])

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

STATUS_OPTIONS = ["🟡 Topic Selected", "🔵 Researching & Outlining", "🟢 Writing Draft", "🏁 Finalized"]

# 1. Private Student Submission Form
with st.form("tracker_form"):
    selected_student = st.selectbox("1. Select your Student Email / ID:", STUDENT_LIST)
    selected_question = st.selectbox("2. Which Assessment Question are you working on?", QUESTION_OPTIONS)
    selected_status = st.selectbox("3. What is your current progress?", STATUS_OPTIONS)
    
    submitted = st.form_submit_button("Submit Selection")

if submitted:
    if selected_student == STUDENT_LIST[0] or selected_question == QUESTION_OPTIONS[0]:
        st.error("⚠️ Please select both your Student Email and an Assignment Question.")
    else:
        # Overwrite previous entry if student re-submits
        df = st.session_state.submissions
        df = df[df["Student Email"] != selected_student]
        
        new_entry = pd.DataFrame([{
            "Student Email": selected_student,
            "Chosen Question": selected_question,
            "Progress Status": selected_status
        }])
        
        st.session_state.submissions = pd.concat([df, new_entry], ignore_index=True)
        
        # Private Confirmation (Only visible to the user submitting right now)
        st.success(f"✅ Selection recorded for **{selected_student}**!")
        st.info(f"**Your Topic:** {selected_question}\n\n**Your Status:** {selected_status}")

# 2. Public Class Overview (Anonymized Data)
st.divider()
st.subheader("📊 Class Topic Overview (Anonymized)")

if st.session_state.submissions.empty:
    st.info("No submissions yet.")
else:
    # Public View: Shows total counts per question without revealing emails
    topic_counts = st.session_state.submissions["Chosen Question"].value_counts().reset_index()
    topic_counts.columns = ["Question / Topic", "Total Students Selected"]
    st.dataframe(topic_counts, use_container_width=True, hide_index=True)

    # Anonymized Table: Masks emails (e.g., 25247104@... -> Student ***7104)
    anon_df = st.session_state.submissions.copy()
    anon_df["Student Email"] = anon_df["Student Email"].apply(lambda x: f"Student ***{x.split('@')[0][-4:]}")
    
    with st.expander("View Anonymized Class Progress"):
        st.dataframe(anon_df[["Student Email", "Chosen Question", "Progress Status"]], use_container_width=True, hide_index=True)
