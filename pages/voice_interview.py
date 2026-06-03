import streamlit as st
from streamlit_mic_recorder import mic_recorder
import os

st.title("🎤 AI Mock Interview")

# -----------------------------
# Resume Input
# -----------------------------
resume_text = st.text_area("Paste Resume Text")

# -----------------------------
# Generate Interview
# -----------------------------
if st.button("Generate Interview"):
    # LAZY LOADING: Import the heavy agent only when the button is clicked
    from agents.interview_agent import generate_questions

    with st.spinner("Generating interview questions..."):
        raw_questions = generate_questions(resume_text)

    questions = []
    for line in raw_questions.split("\n"):
        line = line.strip()
        if len(line) > 5:
            questions.append(line)

    st.session_state.questions = questions
    st.session_state.current_question = 0
    st.session_state.scores = []
    st.rerun()

# -----------------------------
# Interview Flow
# -----------------------------
if "questions" in st.session_state:
    idx = st.session_state.current_question
    questions = st.session_state.questions

    if idx < len(questions):
        question = questions[idx]

        st.subheader(f"Question {idx + 1}")
        st.write(question)

        # -------------------------
        # Ask Question
        # -------------------------
        if st.button("🔊 Hear Question"):
            # LAZY LOADING: Load voice generation only on click
            from agents.voice_agent import generate_audio
            with st.spinner("Generating audio..."):
                audio_file = generate_audio(question)
            st.audio(audio_file)

        # -------------------------
        # Record Answer
        # -------------------------
        st.subheader("🎤 Record Your Answer")
        audio = mic_recorder(
            start_prompt="🎤 Start Recording",
            stop_prompt="⏹ Stop Recording",
            just_once=True,
            use_container_width=True
        )

        if audio:
            st.success("Recording completed in memory!")

            # LAZY LOADING: Load heavy transcription and evaluation modules
            from agents.transcription_agent import transcribe_audio
            from agents.evaluator_agent import evaluate_answer
            from utils.save_results import save_result

            # Pass audio bytes directly or write to a temporary location
            # (Note: local file write might throw an error on read-only cloud filesystems)
            # If transcribe_audio can handle bytes, pass audio["bytes"]. 
            # Otherwise, write locally for the temporary transaction:
            try:
                with open("temp_answer.wav", "wb") as f:
                    f.write(audio["bytes"])
                
                # Speech → Text
                with st.spinner("Transcribing your response..."):
                    answer = transcribe_audio("temp_answer.wav")

                st.subheader("Transcript")
                st.write(answer)

                # AI Evaluation
                with st.spinner("Evaluating answer..."):
                    feedback = evaluate_answer(question, answer)

                st.subheader("AI Feedback")
                st.write(feedback)

                # Save Result
                save_result(question, answer, feedback)
                st.session_state.scores.append(feedback)

                # Clean up the temporary file safely
                if os.path.exists("temp_answer.wav"):
                    os.remove("temp_answer.wav")

            except Exception as e:
                st.error(f"Audio processing workflow failed: {e}")

        # -------------------------
        # Next Question
        # -------------------------
        if st.button("➡ Next Question"):
            st.session_state.current_question += 1
            st.rerun()

    else:
        st.success("🎉 Interview Completed!")
        st.subheader("Final Results")
        for result in st.session_state.scores:
            st.write(result)
