from groq import Groq

client = Groq(
    api_key="YOUR_GROQ_API_KEY"
    
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