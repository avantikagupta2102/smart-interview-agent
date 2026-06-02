from gtts import gTTS

def generate_audio(text):

    tts = gTTS(text)

    tts.save("question.mp3")

    return "question.mp3"