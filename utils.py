
from openai import OpenAI
import os

# IMPORTANT: DO NOT MODIFY THIS FILE

API_KEY = "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"
CLIENT = OpenAI(api_key=API_KEY)

def query_llm(message: str) -> str:
    """
    Provided function to query the LLM.
    Args:
        message: The prompt to send to the LLM
    Returns:
        The LLM's response as a string
    """
    response = CLIENT.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message}
    ]
    )
    return response.choices[0].message.content
    