import os
import streamlit as st
from dotenv import load_dotenv

# 1. Page Configuration MUST be the first Streamlit command executed
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🤖",
    layout="wide"
)

# 2. Define the main application workflow logic
def main_app():
    st.title("🤖 AI Interview Coach & Career Guidance System")

    uploaded_file = st.file_uploader(
        "Upload Your Resume (PDF)",
        type=["pdf"]
    )

    if uploaded_file:
        # Import heavy packages ONLY when a file is actually present to keep things fast
        from utils.pdf_reader import read_pdf
        from graph import app_graph

        with st.spinner("Extracting text from resume..."):
            text = read_pdf(uploaded_file)

        st.success("✅ Resume Uploaded Successfully!")

        # Show Resume Content
        st.subheader("📄 Resume Content")
        with st.expander("View Resume Text"):
            st.write(text)

        # Career Goal
        st.subheader("🎯 Target Role")
        target_role = st.text_input(
            "Enter Your Target Role",
            value="Machine Learning Engineer"
        )

        if st.button("Generate Career Analysis"):
            with st.spinner("Running AI Agents..."):
                result = app_graph.invoke(
                    {
                        "resume_text": text,
                        "target_role": target_role,
                        "analysis": "",
                        "questions": "",
                        "skill_gap": "",
                        "roadmap": ""
                    }
                )

            # Display Results
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

# 3. Explicitly construct your sidebar layout using code declarations
# Replace the filenames below if they don't exactly match what is in your directory
pages = [
    st.Page(main_app, title="Resume Analyzer", icon="🤖"),
    st.Page("pages/EXACT_FILENAME_FROM_TERMINAL_HERE.py", title="Dashboard", icon="📊"),
    st.Page("pages/EXACT_SECOND_FILENAME_HERE.py", title="Voice Mock Interview", icon="🎙️"),
]



# 4. Initialize and display the navigation setup
pg = st.navigation(pages)
pg.run()
