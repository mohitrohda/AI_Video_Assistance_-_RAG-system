from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

llm2 = ChatMistralAI(model = "mistral-small-2506")

llm = ChatGoogleGenerativeAI(model = "gemini-3.5-flash-lite")

response = llm2.invoke("Hello, how are you?")
print(response.content)