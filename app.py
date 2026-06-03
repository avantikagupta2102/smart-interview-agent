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
    
    try:
        cursor.execute("ALTER TABLE history ADD COLUMN score REAL")
    except sqlite3.OperationalError:
        pass
        
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
    st.markdown("#AI Resume Analyzer")
    st.markdown("Extract core skill structures, match requirements, and generate tailored training paths instantly.")
    st.markdown("---")
    
    with st.container(border=True):
        st.markdown("###Upload Document Target")
        uploaded_file = st.file_uploader("Upload your CV or Resume in standard format", type=["pdf"], label_visibility="collapsed")

    if uploaded_file:
        from utils.pdf_reader import read_pdf
        from graph import app_graph

        with st.status("Parsing file metadata layouts...", expanded=True) as status:
            st.write("Extracting character text strings...")
            text = read_pdf(uploaded_file)
            st.write("Constructing internal buffer state tables...")
            status.update(label="Document Processed Successfully!", state="complete", expanded=False)

        with st.expander("View Extracted Resume Characters Log"):
            st.text(text)

        st.markdown("###  Optimization Context")
        with st.container(border=True):
            target_role = st.text_input("Enter Target Role / Employment Field Target Profile:", value="Machine Learning Engineer")

        if st.button("Generate Strategic Career Insights", type="primary"):
            with st.spinner("Invoking Autonomous Multi-Agent Processing Graphs..."):
                result = app_graph.invoke({
                    "resume_text": text, "target_role": target_role,
                    "analysis": "", "questions": "", "skill_gap": "", "roadmap": ""
                })
            
            tab1, tab2, tab3, tab4 = st.tabs(["Profile Analysis", " Interview Pool Questions", "Missing Skill Tracks", "Strategic Roadmap"])
            with tab1: st.info(result["analysis"])
            with tab2: st.success(result["questions"])
            with tab3: st.warning(result["skill_gap"])
            with tab4: st.help(result["roadmap"])
    else:
        st.info(" Please upload a PDF resume document target file to initialize optimization analytics loops.")

def dashboard_page():
    st.markdown("#  Analytics Dashboard")
    st.markdown(f"Welcome back, **{st.session_state.username}**. Verify performance timelines and track score history details.")
    st.markdown("---")
    df = get_user_history(st.session_state.username)
    if df.empty:
        st.warning(" No practice history found for this account. Run an active Voice Mock Interview session to populate metrics loops.")
        return

    with st.container(border=True):
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Total Questions Completed", len(df))
        with m2:
            avg_score = round(df["score"].mean(), 2)
            st.metric("Mean Performance Evaluation Rating", f"{avg_score} / 10")
        with m3:
            unique_days = pd.to_datetime(df["timestamp"]).dt.date.nunique()
            st.metric("Total active practice sessions", unique_days)

    st.markdown("###  Visual Metrics Progress Timelines")
    with st.container(border=True):
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.markdown("**Performance Progression Over Time Logs:**")
            timeline_df = df.copy().sort_values(by="timestamp")
            timeline_df = timeline_df.set_index("timestamp")
            st.line_chart(timeline_df["score"])
            
        with chart_col2:
            st.markdown("**Metric Distribution Cluster Quantities:**")
            score_distribution = df["score"].value_counts().sort_index()
            st.bar_chart(score_distribution)

    st.markdown("### Historic Verification Log Data Archive")
    with st.container(border=True):
        st.dataframe(df, width="stretch")

def voice_interview_page():
    st.markdown("#  Mock Interview Panel")
    st.markdown("Simulate interactive technical question tracking with real-time feedback processing metrics loops.")
    st.markdown("---")
    
    from streamlit_mic_recorder import mic_recorder

    with st.container(border=True):
        st.markdown("###  Set Session Baseline Context")
        resume_text = st.text_area("Paste contextual requirements profile data text here:", height=120)

    if st.button("Generate Interview Evaluation Queue", type="primary"):
        from agents.interview_agent import generate_questions
        with st.spinner("Synthesizing custom simulation scripts..."):
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
            
            st.markdown(f"### Question Profile {idx + 1} of {len(questions)}")
            st.info(question)

            btn_col1, btn_col2 = st.columns([1, 4])
            with btn_col1:
                if st.button("Audio Stream", use_container_width=True):
                    from agents.voice_agent import generate_audio
                    with st.spinner("Synthesizing audio data streams..."):
                        audio_file = generate_audio(question)
                    st.audio(audio_file)

            st.markdown("####  Capture Live Voice Stream")
            audio = mic_recorder(
                start_prompt=" Start Capture", 
                stop_prompt=" Terminate Stream",
                just_once=True
            )

            if audio:
                st.success(" Voice capture successfully saved to runtime buffer space!")
                from agents.transcription_agent import transcribe_audio
                from agents.evaluator_agent import evaluate_answer
                
                with open("temp_answer.wav", "wb") as f:
                    f.write(audio["bytes"])
                
                with st.status("Evaluating response attributes...", expanded=True) as feedback_status:
                    st.write("Transcribing audio tracking matrix waveforms...")
                    answer = transcribe_audio("temp_answer.wav")
                    
                    st.write("Processing language modeling evaluation patterns...")
                    feedback = evaluate_answer(question, answer)
                    feedback_status.update(label="Evaluation Calculations Finished!", state="complete", expanded=False)
                    
                with st.container(border=True):
                    st.markdown("Your Transcription Log Output:")
                    st.write(answer)
                    st.markdown("---")
                    st.markdown("AI Response Feedback Assessment Metric Output:")
                    st.write(feedback)
                    
                computed_score = parse_numerical_score(feedback)
                save_interview_entry(st.session_state.username, question, answer, feedback, computed_score)
                st.session_state.scores.append(computed_score)
                
                if os.path.exists("temp_answer.wav"):
                    os.remove("temp_answer.wav")
                    
            st.markdown("---")
            if st.button("Proceed to Next Question Target ➡", type="primary"):
                st.session_state.current_question += 1
                st.rerun()
        else:
            st.success(" Simulation Ended! Open your Performance Dashboard to view visual metric plots.")

# ==========================================
# 5. CORE ROUTING INFRASTRUCTURE & SECURITY
# ==========================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None

if not st.session_state.authenticated:
    st.title(" Secure Gateway Portal — AI Interview Coach")
    with st.container(border=True):
        auth_mode = st.radio("Access Selection Mode", ["Login Existing Profile", "Create New Identity Account"], horizontal=True)
        form_col1, form_col2 = st.columns(2)
        with form_col1:
            user_input = st.text_input("Username Identification String").strip()
            pass_input = st.text_input("Security Access Password", type="password").strip()
            
        if auth_mode == "Login Existing Profile":
            if st.button("Unlock Dashboard Portal", type="primary"):
                if check_login(user_input, pass_input):
                    st.session_state.authenticated = True
                    st.session_state.username = user_input
                    st.success(f"Access granted. Welcome back {user_input}!")
                    st.rerun()
                else:
                    st.error(" Identification mismatch verification error. Check username or password.")
        else:
            if st.button("Provision New Account Assets", type="primary"):
                if user_input == "" or pass_input == "":
                    st.warning(" Parameter definitions can not contain empty space entities.")
                else:
                    register_user(user_input, pass_input)
                    st.success(" Identity provisioning sequence succeeded! Select 'Login Existing Profile' above to connect.")
else:
    with st.sidebar:
        st.markdown(f"###  Profile: {st.session_state.username}")
        if st.button(" Log out of Session", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
        st.markdown("---")
        
    pg = st.navigation({
        "System Utilities Workspace": [
            st.Page(page=resume_analyzer_page, title="Resume Analyzer", default=True),
            st.Page(page=dashboard_page, title="Performance Dashboard"),
            st.Page(page=voice_interview_page, title="Voice Mock Interview Panel"),
        ]
    }, position="sidebar")
    pg.run()


