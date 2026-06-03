import os
from dotenv import load_dotenv
import streamlit as st

# Load the .env file immediately so all background modules (like graph) can use it
load_dotenv() 

from utils.pdf_reader import read_pdf
from graph import app_graph

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Interview Coach & Career Guidance System")

uploaded_file = st.file_uploader(
    "Upload Your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:

    # Save uploaded PDF
    with open("resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract text
    text = read_pdf("resume.pdf")

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

        # Resume Analysis
        st.subheader("🧠 Resume Analysis")
        st.write(result["analysis"])

        # Interview Questions
        st.subheader("🎯 Interview Questions")
        st.write(result["questions"])

        # Skill Gap Analysis
        st.subheader("📊 Skill Gap Analysis")
        st.write(result["skill_gap"])

        # Learning Roadmap
        st.subheader("🛣 Personalized Learning Roadmap")
        st.write(result["roadmap"])

else:
    st.info("📄 Please upload a PDF resume to begin.")
