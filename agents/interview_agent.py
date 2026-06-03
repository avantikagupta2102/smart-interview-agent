import os
from dotenv import load_dotenv
from groq import Groq

# 1. Load the environment file variables
load_dotenv()

# 2. Grab the actual key dynamically using os.getenv
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_questions(resume_text):

    prompt = f"""
Generate exactly 5 interview questions
based on this resume.

Resume:
{resume_text}

Return only questions.
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
