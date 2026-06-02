import streamlit as st
import pandas as pd
import os

FILE = "data/interview_history.csv"

st.title("📊 Interview Dashboard")

if not os.path.exists(FILE):

    st.warning(
        "No interview data found yet. Complete at least one interview first."
    )

else:

    df = pd.read_csv(FILE)

    st.subheader("Interview History")

    st.dataframe(df)

    st.metric(
        "Total Questions Answered",
        len(df)
    )

    if "score" in df.columns:

        st.metric(
            "Average Score",
            round(df["score"].mean(), 2)
        )