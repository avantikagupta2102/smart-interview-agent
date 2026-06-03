import os
import sys
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# 1. Page Configuration MUST be the first Streamlit command executed
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"  # Force sidebar open on startup
)

load_dotenv()

# ==========================================
# PAGE 1: RESUME ANALYZER SYSTEM
# ==========================================
def resume_analyzer_page():
    st.title("🤖 AI Interview Coach & Career Guidance System")
    uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

    if uploaded_file:
        from utils.pdf_reader import read_pdf
        from graph import app_graph

        with st.spinner("Extracting text from resume..."):
            text = read_pdf(uploaded_file)
        st.success("✅ Resume Uploaded Successfully!")

        with st.expander("View Resume Text"):
            st.write(text)

        st.subheader("🎯 Target Role")
        target_role = st.text_input("Enter Your Target Role", value="Machine Learning Engineer")

        if st.button("Generate Career Analysis"):
            with st.spinner("Running AI Agents..."):
                result = app_graph.invoke({
                    "resume_text": text, "target_role": target_role,
                    "analysis": "", "questions": "", "skill_gap": "", "roadmap": ""
                })
            st.subheader("🧠 Resume Analysis")
            st.write(result["analysis"])
            st.subheader("🎯 Interview Questions")
            st.write(result["questions"])
            st.subheader("📊 Skill Gap Analysis")
            st.write(result["skill_gap"])
            st.subheader("🛣 Personalized Learning Roadmap")
            st.write(result["roadmap"])
    else:
        st.info("📄 Please upload a PDF resume to begin.")

# ==========================================
# PAGE 2: INTERVIEW DASHBOARD METRICS
# ==========================================
def dashboard_page():
    st.title("📊 Interview Dashboard")
    FILE = "data/interview_history.csv"
    
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(FILE) or os.stat(FILE).st_size == 0:
        st.info("📄 No interview history found yet. Complete a voice interview first!")
    else:
        try:
            df = pd.read_csv(FILE)
            st.subheader("Interview History")
            st.dataframe(df, use_container_width=True)
            st.metric("Total Questions Answered", len(df))
        except Exception as e:
            st.error(f"Error loading dashboard: {e}")

# ==========================================
# PAGE 3: VOICE MOCK INTERVIEW CORE
# ==========================================
def voice_interview_page():
    st.title("🎤 AI Mock Interview Panel")
    from streamlit_mic_recorder import mic_recorder

    resume_text = st.text_area("Paste Resume Text")

    if st.button("Generate Interview Questions"):
        from agents.interview_agent import generate_questions
        with st.spinner("Generating questions..."):
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
            st.subheader(f"Question {idx + 1}")
            st.write(question)

            if st.button("🔊 Hear Question"):
                from agents.voice_agent import generate_audio
                with st.spinner("Generating audio..."):
                    audio_file = generate_audio(question)
                st.audio(audio_file)

            st.subheader("🎤 Record Your Answer")
            audio = mic_recorder(
                start_prompt="🎤 Start Recording", stop_prompt="⏹ Stop Recording",
                just_once=True, use_container_width=True
            )

            if audio:
                st.success("Recording completed in memory!")
                from agents.transcription_agent import transcribe_audio
                from agents.evaluator_agent import evaluate_answer
                from utils.save_results import save_result

                try:
                    with open("temp_answer.wav", "wb") as f:
                        f.write(audio["bytes"])
                    
                    with st.spinner("Transcribing..."):
                        answer = transcribe_audio("temp_answer.wav")
                    st.subheader("Transcript")
                    st.write(answer)

                    with st.spinner("Evaluating..."):
                        feedback = evaluate_answer(question, answer)
                    st.subheader("AI Feedback")
                    st.write(feedback)

                    save_result(question, answer, feedback)
                    st.session_state.scores.append(feedback)

                    if os.path.exists("temp_answer.wav"):
                        os.remove("temp_answer.wav")
                except Exception as e:
                    st.error(f"Audio workflow failed: {e}")

            if st.button("➡ Next Question"):
                st.session_state.current_question += 1
                st.rerun()
        else:
            st.success("🎉 Interview Completed!")


# ==========================================
# RESTRUCTURED NAV ROUTING SECTION
# ==========================================
# Declare and tie pages cleanly into Streamlit's routing architecture
pg = st.navigation({
    "Navigation Menu": [
        st.Page(resume_analyzer_page, title="Resume Analyzer", icon="🤖", default=True),
        st.Page(dashboard_page, title="Dashboard", icon="📊"),
        st.Page(voice_interview_page, title="Voice Mock Interview", icon="🎙️"),
    ]
})

# Run routing engine
pg.run()
