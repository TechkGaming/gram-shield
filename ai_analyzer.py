import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def get_ai_analysis(message):

    prompt = f"""
You are Gram-Shield, a cybersecurity assistant designed to protect
villagers from online scams.

Analyze this message:

"{message}"

Identify:
1. Scam category
2. Why the message is suspicious
3. What the user should do

IMPORTANT:
- Detect the language of the message automatically.
- If the message is in Tamil, respond in simple Tamil.
- If the message is in English, respond in simple English.
- Keep the response short and easy for a normal smartphone user to understand.
- Never ask the user to share OTPs, passwords, bank details, Aadhaar numbers, or other sensitive information.
- Clearly warn the user not to click suspicious links.
"""

    response = client.with_options(timeout=60.0).chat.completions.create(
    model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a scam detection and cybersecurity assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=300
    )

    return response.choices[0].message.content