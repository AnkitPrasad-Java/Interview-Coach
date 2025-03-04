import streamlit as st
import ollama
from auth import login, register
from resume_analysis import extract_text_from_pdf, analyze_resume
from evaluator import evaluate_interview
from interviewers import fetch_questions_from_ollama

# Set Page Config
st.set_page_config(page_title="AI Interview Coach", page_icon="🎤", layout="wide")

# Sidebar Navigation
st.sidebar.title("🔹 Navigation")

# User authentication state
if "user" not in st.session_state:
    st.session_state.user = None

# Ensure session state variables are initialized
if "questions" not in st.session_state:
    st.session_state["questions"] = {}
if "answers" not in st.session_state:
    st.session_state["answers"] = {}
if "progress" not in st.session_state:
    st.session_state["progress"] = 0
if "total_questions" not in st.session_state:
    st.session_state["total_questions"] = 0

# Show only login and register options if not logged in
if not st.session_state.user:
    page = st.sidebar.radio("Go to", ["Login", "Register"])
else:
    page = st.sidebar.radio("Go to", ["AI Interview", "Resume Analysis"])
    if st.sidebar.button("Logout ❌"):
        st.session_state.user = None
        st.rerun()

# ✅ Login Page
if page == "Login":
    st.title("🔑 Login to AI Interview Coach")
    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")
    
    if st.button("Login"):
        if login(username, password):
            st.session_state.user = username
            st.success("✅ Logged in successfully!")
            st.rerun()
        else:
            st.error("❌ Invalid Credentials")

# ✅ Registration Page
elif page == "Register":
    st.title("📝 Register for AI Interview Coach")
    new_username = st.text_input("👤 Choose a Username")
    new_password = st.text_input("🔒 Choose a Password", type="password")
    
    if st.button("Register"):
        if register(new_username, new_password):
            st.success("✅ Registration successful! Please login.")
            st.rerun()
        else:
            st.error("❌ Username already exists. Try a different one.")

# ✅ AI Interview Page
elif page == "AI Interview":
    st.title("🎤 Multi-Agent AI Interview")
    job_role = st.selectbox("🎯 Choose Job Role", ["Software Engineer", "Data Scientist", "Finance Analyst", "Marketing Manager"])
    difficulty = st.selectbox("📊 Select Difficulty", ["Easy", "Medium", "Hard"])
    
    interview_types = ["HR Interview", "Technical Interview", "Behavioral Interview"]
    selected_types = st.multiselect("🤖 Select Interview Types", interview_types, default=interview_types)
    
    if st.button("Start Interview"):
        with st.spinner("Generating AI Questions..."):
            st.session_state["questions"] = {}
            st.session_state["answers"] = {}

            for interview_type in selected_types:
                st.session_state["questions"][interview_type] = fetch_questions_from_ollama(job_role, interview_type, difficulty)

            st.session_state["progress"] = 0
            st.session_state["total_questions"] = sum(len(qs) for qs in st.session_state["questions"].values())
            st.rerun()

    if "questions" in st.session_state and st.session_state["questions"]:
        completed_questions = 0
        for interview_type, questions in st.session_state["questions"].items():
            st.write(f"### 📝 {interview_type} Questions:")
            user_answers = []
            for i, question in enumerate(questions, 1):
                st.write(f"{question}")
                answer = st.text_area(f"✍️ Answer {i}", key=f"{interview_type}_answer_{i}")
                if answer:
                    completed_questions += 1
                user_answers.append(answer)
            st.session_state["answers"][interview_type] = user_answers
        
        progress = completed_questions / st.session_state["total_questions"] if st.session_state["total_questions"] else 0
        st.progress(progress)

        for interview_type in st.session_state["questions"]:
            if st.button(f"Evaluate {interview_type}"):
                with st.spinner("Evaluating your responses..."):
                    evaluation_report = evaluate_interview(st.session_state["questions"][interview_type], st.session_state["answers"].get(interview_type, []))
                    st.markdown(f"### 📊 {interview_type} Feedback")
                    st.write(evaluation_report)

# ✅ Resume Analysis Page
elif page == "Resume Analysis":
    st.title("📄 AI Resume Analyzer")
    uploaded_file = st.file_uploader("📤 Upload your Resume (PDF only)", type="pdf")

    if uploaded_file:
        with open("temp_resume.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("✅ Resume uploaded successfully!")

        if st.button("📊 Analyze Resume"):
            with st.spinner("Analyzing..."):
                resume_text = extract_text_from_pdf("temp_resume.pdf")
                feedback = analyze_resume(resume_text)
                st.markdown("### 📌 Resume Analysis Report")
                st.write(feedback)
