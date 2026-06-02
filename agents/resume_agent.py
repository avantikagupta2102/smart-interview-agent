from groq import Groq

client = Groq(
    api_key="YOUR_GROQ_API_KEY"
)

def analyze_resume(text):

    prompt = f"""
    Analyze this resume and provide:

    1. Skills
    2. Projects
    3. Strengths
    4. Weaknesses
    5. Suggested Job Roles
    6. Resume Improvement Tips

    Resume:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content