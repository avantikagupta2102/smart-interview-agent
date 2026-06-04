import streamlit as st
from streamlit_mic_recorder import mic_recorder
import os

st.title("AI Mock Interview")

resume_text = st.text_area("Paste Resume Text")

if st.button("Generate Interview"):
   
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

if "questions" in st.session_state:
    idx = st.session_state.current_question
    questions = st.session_state.questions

    if idx < len(questions):
        question = questions[idx]

        st.subheader(f"Question {idx + 1}")
        st.write(question)

 
        if st.button(" Hear Question"):
            # LAZY LOADING: Load voice generation only on click
            from agents.voice_agent import generate_audio
            with st.spinner("Generating audio..."):
                audio_file = generate_audio(question)
            st.audio(audio_file)

      
        st.subheader(" Record Your Answer")
        audio = mic_recorder(
           start_prompt=" Start Recording", 
           stop_prompt=" Stop Recording",
           just_once=True, 
           width="stretch"
        )

        if audio:
            st.success("Recording completed in memory!")

           
            from agents.transcription_agent import transcribe_audio
            from agents.evaluator_agent import evaluate_answer
            from utils.save_results import save_result

           
            try:
                with open("temp_answer.wav", "wb") as f:
                    f.write(audio["bytes"])
                
              
                with st.spinner("Transcribing your response..."):
                    answer = transcribe_audio("temp_answer.wav")

                st.subheader("Transcript")
                st.write(answer)

              
                with st.spinner("Evaluating answer..."):
                    feedback = evaluate_answer(question, answer)

                st.subheader("AI Feedback")
                st.write(feedback)

             
                save_result(question, answer, feedback)
                st.session_state.scores.append(feedback)

                if os.path.exists("temp_answer.wav"):
                    os.remove("temp_answer.wav")

            except Exception as e:
                st.error(f"Audio processing workflow failed: {e}")

        if st.button("➡ Next Question"):
            st.session_state.current_question += 1
            st.rerun()

    else:
        st.success("Interview Completed!")
        st.subheader("Final Results")
        for result in st.session_state.scores:
            st.write(result)
