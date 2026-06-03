import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_skill_gap(resume_text, target_role):
    prompt = f"""
    Resume:
    {resume_text}

    Target Role:
    {target_role}

    Analyze:

    1. Existing Skills
    2. Missing Skills
    3. Skill Match Percentage
    4. Important Certifications
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {{
                "role": "user",
                "content": prompt
            }}
        ]
    )

    return response.choices[0].message.content
