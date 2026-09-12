import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="Assessment Topic Tracker", page_icon="🎯", layout="centered")

# Custom Styling (Multi-Color Subsection Palette)
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: #0f172a;
    }
    
    /* App Title - Vibrant Amber/Orange */
    .main-title {
        color: #f59e0b;
        font-family: 'Inter', sans-serif;
        font-size: 2.6rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
    }
    .sub-title {
        color: #cbd5e1;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* Main Form Container */
    [data-testid="stForm"] {
        background: #172554;
        border-radius: 20px;
        padding: 30px;
        border: 2px solid #3b82f6;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
    }
    
    /* --- SUBSECTION 1: GREEN (Student ID) --- */
    .sub-box-1 {
        background: #064e3b;
        border-left: 6px solid #10b981;
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .sub-box-1 label {
        color: #a7f3d0 !important;
        font-size: 1.2rem !important;
        font-weight: 800 !important;
    }
    
    /* --- SUBSECTION 2: PURPLE (Question Selection) --- */
    .sub-box-2 {
        background: #3b0764;
        border-left: 6px solid #a855f7;
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .sub-box-2 label {
        color: #e9d5ff !important;
        font-size: 1.2rem !important;
        font-weight: 800 !important;
    }
    
    /* --- SUBSECTION 3: PINK (Progress Stage) --- */
    .sub-box-3 {
        background: #831843;
        border-left: 6px solid #f43f5e;
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 25px;
    }
    .sub-box-3 label {
        color: #fecdd3 !important;
        font-size: 1.2rem !important;
        font-weight: 800 !important;
    }
    
    /* SUBMIT BUTTON - CORAL GRADIENT */
    div.stButton > button {
        background: linear-gradient(90deg, #f97316 0%, #ef4444 100%) !important;
        color: #ffffff !important;
        font-size: 1.3rem !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        border: none !important;
        width: 100%;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.4);
    }
    div.stButton > button:hover {
        transform: scale(1.01);
        box-shadow: 0 6px 25px rgba(239, 68, 68, 0.6);
    }
    
    /* OVERVIEW SECTION - TEAL */
    .section-header-teal {
        color: #2dd4bf;
        font-size: 1.7rem;
        font-weight: 800;
        margin-top: 35px;
        margin-bottom: 15px;
        text-shadow: 0 0 10px rgba(45, 212, 191, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Main Titles
st.markdown('<p class="main-title">🎯 Assessment Topic Tracker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Arden University • Register & Track Your Assessment Topic</p>', unsafe_allow_html=True)

# Shared Data Storage
if "submissions" not in st.session_state:
    st.session_state.submissions = pd.DataFrame(columns=["Student Email", "Chosen Question", "Progress Status"])

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
    
    # Subsection 1: Green Box
    st.markdown('<div class="sub-box-1">', unsafe_allow_html=True)
    user_email_input = st.text_input(
        "1. Enter Your Arden Student ID or Email:", 
        placeholder="e.g., 26102538"
    ).strip().lower()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Subsection 2: Purple Box
    st.markdown('<div class="sub-box-2">', unsafe_allow_html=True)
    selected_question = st.selectbox("2. Which Assessment Question Are You Working On?", QUESTION_OPTIONS)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Subsection 3: Pink Box
    st.markdown('<div class="sub-box-3">', unsafe_allow_html=True)
    selected_status = st.selectbox("3. What Is Your Current Progress Stage?", STATUS_OPTIONS)
    st.markdown('</div>', unsafe_allow_html=True)
    
    submitted = st.form_submit_button("🚀 Submit Selection")

# Form Processing Logic
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
st.markdown('<h3 class="section-header-teal">📊 Class Topic Overview</h3>', unsafe_allow_html=True)

if st.session_state.submissions.empty:
    st.info("No submissions logged yet. Be the first to register your topic!")
else:
    topic_counts = st.session_state.submissions["Chosen Question"].value_counts().reset_index()
    topic_counts.columns = ["Question / Topic", "Total Students Selected"]
    st.dataframe(topic_counts, use_container_width=True, hide_index=True)
