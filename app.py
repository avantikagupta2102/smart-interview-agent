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


# 3. Dynamic Page Scanner Layout
# This automatically searches your pages folder and loads your exact subpages securely!
pages_dir = "pages"
discovered_pages = [st.Page(main_app, title="Resume Analyzer", icon="🤖")]

if os.path.exists(pages_dir):
    for file in sorted(os.listdir(pages_dir)):
        if file.endswith(".py") and not file.startswith("__"):
            # Format a clean title from the filename string (e.g. "voice_interview" -> "Voice interview")
            clean_title = file.replace(".py", "").replace("_", " ").capitalize()
            
            # Dynamically attach an appropriate sidebar icon
            page_icon = "🎙️" if "voice" in file.lower() or "interview" in file.lower() else "📊"
            
            # Map and append the file configuration cleanly
            discovered_pages.append(
                st.Page(os.path.join(pages_dir, file), title=clean_title, icon=page_icon)
            )


# 4. Initialize and display the navigation setup
pg = st.navigation(discovered_pages)
pg.run()
