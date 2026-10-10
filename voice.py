from gtts import gTTS
import os


def generate_tamil_warning():
    text = (
        "எச்சரிக்கை. இந்த செய்தி மோசடியாக இருக்கலாம். "
        "தயவுசெய்து இந்த இணைப்பை திறக்க வேண்டாம். "
        "உங்கள் OTP, கடவுச்சொல் அல்லது வங்கி தகவல்களை யாரிடமும் பகிர வேண்டாம்."
    )

    filename = "warning_tamil.mp3"

    tts = gTTS(
        text=text,
        lang="ta"
    )

    tts.save(filename)

    return filename