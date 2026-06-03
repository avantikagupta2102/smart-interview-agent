import os
from dotenv import load_dotenv
from groq import Groq

# 1. Load the environment file variables
load_dotenv()

# 2. Grab the actual key using os.getenv instead of using a hardcoded string
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def evaluate_answer(question, answer):

    prompt = f"""
Question:
{question}

Answer:
{answer}

Evaluate:

1. Technical Score (/10)
2. Communication Score (/10)
3. Overall Score (/10)

Give strengths and weaknesses.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response.choices[0].message.content
