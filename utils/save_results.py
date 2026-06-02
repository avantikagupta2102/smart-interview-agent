import pandas as pd
import os
from datetime import datetime
from utils.score_parser import extract_score

# Create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

FILE = "data/interview_history.csv"


def save_result(question, answer, feedback):

    print("SAVE_RESULT CALLED")

    score = extract_score(feedback)

    row = {
        "date": str(datetime.now()),
        "question": question,
        "answer": answer,
        "score": score,
        "feedback": feedback
    }

    columns = [
        "date",
        "question",
        "answer",
        "score",
        "feedback"
    ]

    try:

        if os.path.exists(FILE) and os.path.getsize(FILE) > 0:

            df = pd.read_csv(FILE)

        else:

            df = pd.DataFrame(columns=columns)

    except Exception as e:

        print("CSV Read Error:", e)

        df = pd.DataFrame(columns=columns)

    df = pd.concat(
        [df, pd.DataFrame([row])],
        ignore_index=True
    )

    df.to_csv(FILE, index=False)

    print(f"Saved interview result to {FILE}")