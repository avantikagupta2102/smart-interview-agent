from groq import Groq

client = Groq(
    api_key="YOUR_GROQ_API_KEY"
)

def generate_roadmap(skill_gap_report):

    prompt = f"""
    Based on this skill gap report:

    {skill_gap_report}

    Create:

    1. 8 Week Learning Roadmap
    2. Topics Week Wise
    3. Resources To Learn
    4. Final Project Suggestion
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