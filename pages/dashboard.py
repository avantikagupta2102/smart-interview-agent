import streamlit as st
import pandas as pd
import os

FILE = "data/interview_history.csv"

st.title("📊 Interview Dashboard")

# Ensure the data folder exists so the cloud server doesn't throw a path error
if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(FILE) or os.stat(FILE).st_size == 0:
    # Initialize an empty file with standard columns if it doesn't exist yet
    df_empty = pd.DataFrame(columns=["date", "question", "answer", "score"])
    df_empty.to_csv(FILE, index=False)
    
    st.info(
        "📄 No interview history found yet. Complete a voice mock interview to populate your statistics!"
    )
else:
    try:
        df = pd.read_csv(FILE)
        
        if df.empty:
            st.info("📄 Complete at least one interview first to populate the dashboard metrics.")
        else:
            st.subheader("Interview History")
            st.dataframe(df, width="stretch")

            # Dashboard KPIs
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label="Total Questions Answered",
                    value=len(df)
                )

            with col2:
                if "score" in df.columns and not df["score"].isnull().all():
                    st.metric(
                        label="Average Score",
                        value=f"{round(pd.to_numeric(df['score'], errors='coerce').mean(), 2)} / 10"
                    )
                else:
                    st.metric(label="Average Score", value="N/A")
    except Exception as e:
        st.error(f"Error loading dashboard data matrix: {e}")
