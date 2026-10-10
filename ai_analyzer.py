import os
from dotenv import load_dotenv
from groq import Groq, GroqError

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key) if api_key else None


def get_ai_analysis(message):

    if client is None:
        return "Groq API key missing. Check your .env file."

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
- Detect the language automatically.
- If Tamil, respond in simple Tamil.
- If English, respond in simple English.
- Keep the response short and easy to understand.
- Never ask for OTPs, passwords, bank details, or Aadhaar numbers.
- Warn users not to click suspicious links.
"""

    try:
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

    except GroqError as e:
        print(f"Groq API error: {type(e).__name__}: {e}")
        return "AI analysis is temporarily unavailable. Please try again."
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")
        return "An unexpected error occurred during AI analysis."
