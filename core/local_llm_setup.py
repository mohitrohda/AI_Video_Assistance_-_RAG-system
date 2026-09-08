from langchain_openai import ChatOpenAI
import os

def get_llm():
    return ChatOpenAI(
        base_url="http://127.0.0.1:8080",
        api_key="not-needed",
        model="Qwen2.5-Coder-3B-Instruct",
        temperature=0.3,
    )