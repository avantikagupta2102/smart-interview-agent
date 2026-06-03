import os
from dotenv import load_dotenv
from groq import Groq

# 1. Load the environment file variables
load_dotenv()

# 2. Grab the actual key dynamically using os.getenv
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def transcribe_audio(path):

    with open(path, "rb") as file:

        transcript = client.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3"
        )

    return transcript.text
