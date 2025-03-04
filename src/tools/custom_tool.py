from textblob import TextBlob
from langchain.tools import Tool
from model.ollama_model import OllamaHandler
from tools.weather_tool import get_weather
from tools.stock_tool import get_stock_price
from tools.internet_search_tool import search_internet

# Initialize the Ollama model for direct conversation
ollama_handler = OllamaHandler()


def is_greeting(query: str) -> bool:
    """
    Detects if the input query is a greeting by analyzing the sentence structure and meaning.
    """
    analysis = TextBlob(query)
    words = analysis.words.lower()
    
    if "hello" in words or "hi" in words or "hallo" in words or analysis.sentiment.polarity > 0.5:
        return True
    return False


def custom_response_tool(query: str) -> str:
    """
    Analyzes user queries and directs them to the appropriate tool if available.
    If no suitable tool is found, initiates a live chat session.
    """
    query_lower = query.lower().strip()

    # التحقق مما إذا كان الإدخال تحية
    if is_greeting(query_lower):
        return "Hello! How can I assist you today?"

    words = query_lower.split()

    # Check for weather queries
    if any(keyword in query_lower for keyword in ["weather", "temperature", "forecast"]):
        city = words[-1] if words else "unknown location"
        return get_weather(city)

    # Check for stock price queries
    if any(keyword in query_lower for keyword in ["stock", "price", "share"]) or query.isupper():
        return get_stock_price(query)

    # Check for internet search queries
    if len(words) > 1 or query.isalpha():
        return search_internet(query)

    # Initiate live chat mode if no tool matches
    print("\nAI Assistant is now in live chat mode. Type 'exit' to end the chat.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting live chat mode.")
            return "Live chat session ended."

        response = ollama_handler.get_response(user_input)
        print(f"AI: {response}")


# Register the tool
custom_tool = Tool(
    name="GeneralResponse",
    func=custom_response_tool,
    description="Handles queries dynamically and starts a live chat session if no tool matches.",
    return_direct=True,
)
