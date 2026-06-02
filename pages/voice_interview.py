import streamlit as st

from streamlit_mic_recorder import mic_recorder

from agents.voice_agent import generate_audio
from agents.interview_agent import generate_questions
from agents.evaluator_agent import evaluate_answer
from agents.transcription_agent import transcribe_audio

from utils.save_results import save_result

st.title("🎤 AI Mock Interview")

# -----------------------------
# Resume Input
# -----------------------------

resume_text = st.text_area(
    "Paste Resume Text"
)

# -----------------------------
# Generate Interview
# -----------------------------

if st.button("Generate Interview"):

    raw_questions = generate_questions(
        resume_text
    )

    questions = []

    for line in raw_questions.split("\n"):

        line = line.strip()

        if len(line) > 5:

            questions.append(line)

    st.session_state.questions = questions

    st.session_state.current_question = 0

    st.session_state.scores = []

# -----------------------------
# Interview Flow
# -----------------------------

if "questions" in st.session_state:

    idx = st.session_state.current_question

    questions = st.session_state.questions

    if idx < len(questions):

        question = questions[idx]

        st.subheader(
            f"Question {idx + 1}"
        )

        st.write(question)

        # -------------------------
        # Ask Question
        # -------------------------

        if st.button("🔊 Hear Question"):

            audio_file = generate_audio(
                question
            )

            st.audio(audio_file)

        # -------------------------
        # Record Answer
        # -------------------------

        st.subheader(
            "🎤 Record Your Answer"
        )

        audio = mic_recorder(
            start_prompt="🎤 Start Recording",
            stop_prompt="⏹ Stop Recording",
            just_once=True,
            use_container_width=True
        )

        if audio:

            with open(
                "temp_answer.wav",
                "wb"
            ) as f:

                f.write(
                    audio["bytes"]
                )

            st.success(
                "Recording completed!"
            )

            # ---------------------
            # Speech → Text
            # ---------------------

            answer = transcribe_audio(
                "temp_answer.wav"
            )

            st.subheader(
                "Transcript"
            )

            st.write(answer)

            # ---------------------
            # AI Evaluation
            # ---------------------

            with st.spinner(
                "Evaluating answer..."
            ):

                feedback = evaluate_answer(
                    question,
                    answer
                )

            st.subheader(
                "AI Feedback"
            )

            st.write(feedback)

            # ---------------------
            # Save Result
            # ---------------------

            save_result(
                question,
                answer,
                feedback
            )

            st.session_state.scores.append(
                feedback
            )

        # -------------------------
        # Next Question
        # -------------------------

        if st.button("➡ Next Question"):

            st.session_state.current_question += 1

            st.rerun()

    else:

        st.success(
            "🎉 Interview Completed!"
        )

        st.subheader(
            "Final Results"
        )

        for result in st.session_state.scores:

            st.write(result)