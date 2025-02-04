
from openai import OpenAI
import os

# IMPORTANT: DO NOT MODIFY THIS FILE

API_KEY = "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"
CLIENT = OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")

def query_llm(message: str) -> str:
    """
    Provided function to query the LLM.
    Args:
        message: The prompt to send to the LLM
    Returns:
        The LLM's response as a string
    """
    response = CLIENT.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message}
    ]
    )
    return response.choices[0].message.content
    