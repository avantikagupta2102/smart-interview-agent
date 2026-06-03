import os
import streamlit as st
from dotenv import load_dotenv

# 1. Page Configuration MUST be the first Streamlit command executed
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🤖",
    layout="wide"
)

# Force the Streamlit sidebar to stay open and visible permanently on all monitors
st.markdown(
    """
    <style>
        /* Uncollapse the sidebar container */
        [data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }
        section[data-testid="stSidebar"] {
            left: 0 !important;
            visibility: visible !important;
            width: 250px !important;
        }
        /* Adjust the main content block to sit comfortably next to the open sidebar */
        .main .block-container {
            margin-left: 20px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the environment keys globally
load_dotenv() 

# 2. Page 1: Resume Analyzer
def main_app():
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

# 3. Page 2: Dashboard (Imported directly to bypass folder issues)
def dashboard_app():
    try:
        from pages.dashboard import FILE
        import pandas as pd
        
        st.title("📊 Interview Dashboard")
        if not os.path.exists("data"):
            os.makedirs("data")
            
        if not os.path.exists(FILE) or os.stat(FILE).st_size == 0:
            st.info("📄 No interview history found yet. Complete a voice interview first!")
        else:
            df = pd.read_csv(FILE)
            st.subheader("Interview History")
            st.dataframe(df, use_container_width=True)
            st.metric("Total Questions Answered", len(df))
    except Exception as e:
        st.error(f"Could not load dashboard view: {e}")

# 4. Page 3: Voice Interview (Imported directly to bypass folder issues)
def voice_app():
    try:
        # This executes the interior layout of your voice script safely
        import sys
        if 'pages.voice_interview' in sys.modules:
            del sys.modules['pages.voice_interview']
        import pages.voice_interview
    except Exception as e:
        # If case-sensitivity is flipped on the server, catch the alternate name
        try:
            import pages.Voice_interview
        except:
            st.error(f"Could not load voice view: {e}")

# 5. Build the Hardcoded Sidebar Navigation Menu
pages = [
    st.Page(main_app, title="Resume Analyzer", icon="🤖"),
    st.Page(dashboard_app, title="Dashboard", icon="📊"),
    st.Page(voice_app, title="Voice Mock Interview", icon="🎙️"),
]

# 6. Initialize and display the navigation setup
pg = st.navigation(pages)
pg.run()
