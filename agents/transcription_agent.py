from groq import Groq

client = Groq(
    api_key="YOUR_GROQ_API_KEY"
    
)

def transcribe_audio(path):

    with open(path, "rb") as file:

        transcript = client.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3"
        )

    return transcript.text