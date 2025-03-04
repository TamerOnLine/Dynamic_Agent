from langchain_community.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("YOUR_OPENAI_API_KEY")
if not api_key:
    print("API Key not found!")
else:
    print("API Key Loaded!")

try:
    llm = ChatOpenAI(model_name="gpt-4", openai_api_key=api_key)
    response = llm.invoke("Hello, how are you?")
    print(response)
except Exception as e:
    print(f"Error: {e}")
