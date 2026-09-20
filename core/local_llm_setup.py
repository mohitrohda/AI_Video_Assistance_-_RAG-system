from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
import os


'''
def get_llm():
    return ChatOpenAI(
        base_url="http://127.0.0.1:8080",
        api_key="not-needed",
        model="Qwen2.5-3B-Instruct-Q8_0-GGUF",
        temperature=0.3,
    )

'''

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

