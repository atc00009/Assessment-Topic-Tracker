import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(page_title="Assessment Topic Tracker", page_icon="📝", layout="centered")

# CSS targeting ALL Streamlit text inputs, dropdowns, and buttons
st.markdown("""
    <style>
    /* 1. Page Background (Bright White) */
    .stApp {
        background-color: #ffffff !important;
    }
    
    /* 2. Title & Subtitle */
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
    
    /* 3. Main Form Outer Card */
    [data-testid="stForm"] {
        background-color: #fefce8 !important;
        border: 3px solid #f59e0b !important;
        border-radius: 16px !important;
        padding: 30px !important;
    }
    
    /* 4. Question Labels */
    [data-testid="stForm"] label p {
        color: #b45309 !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
    }
    
    /* 5. FORCE ALL INPUT BOXES & DROPDOWNS TO ASH GREY */
    .stTextInput input,
    .stSelectbox div[data-baseweb="select"],
    .stSelectbox div[data-baseweb="select"] > div,
    div[data-baseweb="select"] {
        background-color: #e2e8f0 !important; /* Soft Ash Grey */
        color: #0f172a !important;            /* Dark Charcoal Text */
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 8px !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
    }

    /* Selected Dropdown Item Text */
    .stSelectbox div[data-baseweb="select"] * {
        color: #0f172a !important;
    }

    /* Placeholder Text */
    .stTextInput input::placeholder {
        color: #64748b !important;
    }

    /* Dropdown Options List Popup */
    ul[data-baseweb="menu"], 
    ul[data-baseweb="menu"] * {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
    }
    
    /* 6. FORCE SUBMIT BUTTON TO ASH GREY WITH BOLD TEXT */
    div[data-testid="stForm"] button,
    div[data-testid="stForm"] button * {
        background-color: #cbd5e1 !important; /* Light Ash Grey Button */
        color: #0f172a !important;            /* Dark Charcoal Text */
        border: 2px solid #94a3b8 !important;
        border-radius: 10px !important;
        font-size: 1.3rem !important;
        font-weight: 900 !important;
        padding: 8px 16px !important;
        width: 100% !important;
        margin-top: 10px !important;
    }

    div[data-testid="stForm"] button:hover {
        background-color: #94a3b8 !important;
        color: #ffffff !important;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Main Titles
st.markdown('<p class="main-title">📝 Assessment Topic Tracker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Arden University • Register & Track Your Topic Choice</p>', unsafe_allow_html=True)

# Session Storage
if "submissions" not in st.session_state:
    st.session_state.submissions = pd.DataFrame(columns=["Student Email", "Chosen Question", "Progress Status"])

# Master Validation List
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
    user_email_input = st.text_input("1. Enter Your Arden Student ID or Email:", placeholder="e.g., 26102538").strip().lower()
    selected_question = st.selectbox("2. Which Assessment Question Are You Working On?", QUESTION_OPTIONS)
    selected_status = st.selectbox("3. What Is Your Current Progress Stage?", STATUS_OPTIONS)
    
    submitted = st.form_submit_button("Submit Selection")

if submitted:
    formatted_email = user_email_input if "@" in user_email_input else f"{user_email_input}@ardenuniversity.ac.uk"
    
    if not user_email_input:
        st.error("⚠️ Please enter your Student ID or Email.")
    elif formatted_email not in [e.lower() for e in VALID_STUDENTS]:
        st.error("❌ Student ID not recognized.")
    elif selected_question == QUESTION_OPTIONS[0]:
        st.error("⚠️ Please select an assessment question.")
    else:
        df = st.session_state.submissions
        df = df[df["Student Email"].str.lower() != formatted_email]
        new_entry = pd.DataFrame([{"Student Email": formatted_email, "Chosen Question": selected_question, "Progress Status": selected_status}])
        st.session_state.submissions = pd.concat([df, new_entry], ignore_index=True)
        st.success(f"✅ Selection logged for **{formatted_email}**!")

st.divider()
st.subheader("📊 Class Topic Overview")
if not st.session_state.submissions.empty:
    topic_counts = st.session_state.submissions["Chosen Question"].value_counts().reset_index()
    topic_counts.columns = ["Question / Topic", "Total Students Selected"]
    st.dataframe(topic_counts, use_container_width=True, hide_index=True)
