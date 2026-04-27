from groq import Groq 
import streamlit as st

client = Groq(api_key = st.secrets["Groq_API"])


SYSTEM_PROMPT = """
    You are a Resume Analyzer AI
    Give Your best to analyze resume.
    Use Bullet points(•)
    Never use '*'

    Give:
    1. Short Summary
    2. Key Skills 
    3. 3 improvements
"""

MODEL="openai/gpt-oss-safeguard-20b"

def ask_ai(prompt):

    full_prompt = f"{SYSTEM_PROMPT}\nUser: {prompt}"
    response = client.chat.completions.create(
            model = MODEL,
            messages = [{"role": "user", "content": prompt}]
        )
    return response.choices[0].message.content

