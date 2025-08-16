# utils/groq_wrapper.py
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_groq(model_id, messages, temperature=0.7):
    response = client.chat.completions.create(
        model=model_id,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content
