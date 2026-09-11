from langchain_openai import ChatOpenAI
import os

def get_llm():
    return ChatOpenAI(
        base_url="http://127.0.0.1:8080",
        api_key="not-needed",
        model="Qwen2.5-3B-Instruct-Q8_0-GGUF",
        temperature=0.3,
    )