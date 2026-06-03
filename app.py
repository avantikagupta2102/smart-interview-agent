import os
import sys
import sqlite3
import re
from datetime import datetime
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# ==========================================
# 1. CORE PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AI Interview Coach Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()

# ==========================================
# 2. DATABASE ORCHESTRATION LAYER (SQLITE)
# ==========================================
DB_FILE = "data/interview_coach.db"

def init_db():
    if not os.path.exists("data"):
        os.makedirs("data")
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            timestamp TEXT,
            question TEXT,
            answer TEXT,
            feedback TEXT,
            score REAL,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    """)
    
    # DATABASE MIGRATION SYSTEM: Forcefully add 'score' column if older database exists
    try:
        cursor.execute("ALTER TABLE history ADD COLUMN score REAL")
    except sqlite3.OperationalError:
        pass # Column already exists, safe to ignore
        
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 3. HELPER UTILITY FUNCTIONS
# ==========================================
def register_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()
    return True

def check_login(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    if user is not None:
        return True
    return False

def save_interview_entry(username, question, answer, feedback, score):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO history (username, timestamp, question, answer, feedback, score)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, timestamp, question, answer, feedback, score))
    conn.commit()
    conn.close()

def get_user_history(username):
    conn = sqlite3.connect(DB_FILE)
    # FIX: Correctly pass the username variable inside the params argument as a list
    df = pd.read_sql_query(
        sql="SELECT timestamp, question, answer, feedback, score FROM history WHERE username = ?", 
        con=conn, 
        params=[username]
    )
    conn.close()
    return df

def parse_numerical_score(feedback_text):
    match = re.search(r"(\d+)\s*/\s*10", feedback_text)
    if match:
        return float(match.group(1))
    match_pct = re.search(r"(\d+)%", feedback_text)
    if match_pct:
        return float(match_pct.group(1)) / 10.0
    return 7.0

# ==========================================
# 4. STREAMLIT APPLICATION INTERFACE PAGES
# ==========================================

def resume_analyzer_page():
    st.markdown("## 🤖 AI Resume Analyzer & Career Guidance")
    st.info("Upload your industry CV/Resume below to extract critical structural career mappings.")
    
    uploaded_file = st.file_uploader("Upload Your Resume (PDF Only)", type=["pdf"])

    if uploaded_file:
        from utils.pdf_reader import read_pdf
        from graph import app_graph

        with st.spinner("Processing document layout structures..."):
            text = read_pdf(uploaded_file)
        st.success("✅ Document Processing Complete!")

        with st.expander("🔍 View Parsed Resume String Content"):
            st.text(text)

        st.subheader("🎯 Optimization Targets")
        target_role = st.text_input("Target Employment Specification Role", value="Machine Learning Engineer")

        if st.button("Generate Strategic Career Insights"):
            with st.spinner("Invoking Autonomous Multi-Agent Graphs..."):
                result = app_graph.invoke({
                    "resume_text": text, "target_role": target_role,
                    "analysis": "", "questions": "", "skill_gap": "", "roadmap": ""
                })
            
            tab1, tab2, tab3, tab4 = st.tabs(["🧠 Comprehensive Analysis", "🎯 Targeted Questions", "📊 Core Skill Gaps", "🛣 Strategy Roadmap"])
            with tab1: 
                st.write(result["analysis"])
            with tab2: 
                st.write(result["questions"])
            with tab3: 
                st.write(result["skill_gap"])
            with tab4: 
                st.write(result["roadmap"])
    else:
        st.info("📄 Please upload a PDF resume file to initialize the tracking dashboard.")

def dashboard_page():
    st.markdown(f"## 📊 Personal Analytics Dashboard — **{st.session_state.username}**")
    
    df = get_user_history(st.session_state.username)
    
    if df.empty:
        st.warning("📄 No historical logs found for this account. Run an active Voice Interview panel session to generate visual logs.")
        return

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Answers Analyzed", len(df))
    with m2:
        avg_score = round(df["score"].mean(), 2)
        st.metric("Mean Performance Rating", f"{avg_score} / 10")
    with m3:
        unique_days = pd.to_datetime(df["timestamp"]).dt.date.nunique()
        st.metric("Active Interview Practice Days", unique_days)

    st.markdown("---")
    
    st.subheader("📈 Visual Performance Progress Timeline")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.write("📉 **Score Progress Over Time**")
        timeline_df = df.copy().sort_values(by="timestamp")
        timeline_df = timeline_df.set_index("timestamp")
        st.line_chart(timeline_df["score"])
        
    with chart_col2:
        st.write("🎯 **Score Distribution**")
        score_distribution = df["score"].value_counts().sort_index()
        st.bar_chart(score_distribution)

    st.markdown("---")
    
    st.subheader("📋 Comprehensive Historic Verification Archive Log")
    st.dataframe(df, width="stretch")

def voice_interview_page():
    st.markdown("## 🎙️ AI Mock Interview Simulation Environment Panel")
    from streamlit_mic_recorder import mic_recorder

    resume_text = st.text_area("Input Base Text Context / CV String", height=150)

    if st.button("Generate Interview Session Evaluation Queue"):
        from agents.interview_agent import generate_questions
        with st.spinner("Generating specialized technical evaluation strings..."):
            raw_questions = generate_questions(resume_text)

        questions = [line.strip() for line in raw_questions.split("\n") if len(line.strip()) > 5]
        st.session_state.questions = questions
        st.session_state.current_question = 0
        st.session_state.scores = []
        st.rerun()

    if "questions" in st.session_state:
        idx = st.session_state.current_question
        questions = st.session_state.questions

        if idx < len(questions):
            question = questions[idx]
            
            st.markdown(f"### ❓ Current Question {idx + 1} of {len(questions)}")
            st.info(question)

            if st.button("🔊 Play Audio Stream Module"):
                from agents.voice_agent import generate_audio
                with st.spinner("Synthesizing dynamic audio flow structure..."):
                    audio_file = generate_audio(question)
                st.audio(audio_file)

            st.markdown("#### 🎤 Capture Live Voice Audio Input Capture")
            audio = mic_recorder(
                start_prompt="🎤 Start Capture", stop_prompt="⏹ Terminate Stream",
                just_once=True, width="stretch"
            )

            if audio:
                st.success("✅ Voice stream successfully captured to memory context buffer!")
                from agents.transcription_agent import transcribe_audio
                from agents.evaluator_agent import evaluate_answer
                
                with open("temp_answer.wav", "wb") as f:
                    f.write(audio["bytes"])
                
                with st.spinner("Processing Voice-To-Text Audio Transcriptions..."):
                    answer = transcribe_audio("temp_answer.wav")
                st.markdown("**Your Captured Transcript:**")
                st.write(answer)

                with st.spinner("Calculating Critical Evaluation Metrics..."):
                    feedback = evaluate_answer(question, answer)
                st.markdown("**AI Response Feedback Assessment Metric Output:**")
                st.write(feedback)

                computed_score = parse_numerical_score(feedback)
                
                save_interview_entry(st.session_state.username, question, answer, feedback, computed_score)
                st.session_state.scores.append(computed_score)

                if os.path.exists("temp_answer.wav"):
                    os.remove("temp_answer.wav")

            if st.button("Proceed to Next Question ➡"):
                st.session_state.current_question += 1
                st.rerun()
        else:
            st.success("🎉 Simulation Ended! Proceed to the Performance Dashboard to verify historical timeline logs.")

# ==========================================
# 5. CORE ROUTING INFRASTRUCTURE & SECURITY
# ==========================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None

if not st.session_state.authenticated:
    st.title("🔐 Secure Gateway Portal — AI Interview Coach")
    auth_mode = st.radio("Access Selection Mode", ["Login Existing Profile", "Create New Identity Account"], horizontal=True)
    
    form_col1, form_col2 = st.columns(2)
    with form_col1:
        user_input = st.text_input("Username Identification String").strip()
        pass_input = st.text_input("Security Access Password", type="password").strip()
        
    if auth_mode == "Login Existing Profile":
        if st.button("Unlock Dashboard Portal"):
            if check_login(user_input, pass_input):
                st.session_state.authenticated = True
                st.session_state.username = user_input
                st.success(f"Access granted. Welcome back {user_input}!")
                st.rerun()
            else:
                st.error("❌ Identification mismatch verification error. Check username or password.")
    else:
        if st.button("Provision New Account Assets"):
            if user_input == "" or pass_input == "":
                st.warning("⚠️ Parameter definitions can not contain empty space entities.")
            else:
                register_user(user_input, pass_input)
                st.success("🎉 Identity provisioning sequence succeeded! Select 'Login Existing Profile' above to connect.")
else:
    with st.sidebar:
        st.markdown(f"### 👤 Profile: {st.session_state.username}")
        if st.button("🔒 Log out of Session"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
        st.markdown("---")
        
    pg = st.navigation({
        "System Utilities Workspace": [
            st.Page(page=resume_analyzer_page, title="Resume Analyzer", icon="🤖", default=True),
            st.Page(page=dashboard_page, title="Performance Dashboard", icon="📊"),
            st.Page(page=voice_interview_page, title="Voice Mock Interview Panel", icon="🎙️"),
        ]
    }, position="sidebar")
    pg.run()
