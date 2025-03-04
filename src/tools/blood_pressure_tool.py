import os
import logging
from langchain.tools import Tool
from serpapi import GoogleSearch
from dotenv import load_dotenv
from tools.internet_search_tool import search_internet  # Import general search tool

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Retrieve SerpAPI API key from environment variables
API_KEY = os.getenv("SERPAPI_API_KEY")

def search_blood_pressure_diseases(query: str) -> str:
    """Search the internet for blood pressure-related diseases using SerpAPI."""
    if not API_KEY:
        logging.error("API_KEY for SerpAPI is missing. Please check your .env file.")
        return "API_KEY for SerpAPI is missing. Please check your .env file."
    
    logging.info(f"Searching for blood pressure-related diseases: {query}")
    params = {
        "q": f"{query} blood pressure disease",
        "api_key": API_KEY,
        "num": 5,
        "hl": "en",
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict().get("organic_results", [])
        
        if not results:
            logging.warning("No relevant results found.")
            return "No relevant results found."
        
        logging.info("Successfully retrieved search results.")
        return "\n".join([f"{r['title']}: {r['link']}" for r in results]) + "\n"
    except Exception as e:
        logging.error(f"Error during search: {e}")
        return "An error occurred while searching for blood pressure-related diseases."

# Define the blood pressure search tool
blood_pressure_tool = Tool(
    name="BloodPressureSearch",
    func=search_blood_pressure_diseases,
    description="Searches for diseases related to blood pressure using SerpAPI.",
    return_direct=True,
)

def custom_response_tool(query: str) -> str:
    """Analyzes user queries and directs them to the appropriate tool."""
    query_lower = query.lower().strip()
    logging.info(f"Processing query: {query_lower}")
    words = query_lower.split()

    # Check for blood pressure disease queries
    if any(keyword in query_lower for keyword in ["blood pressure", "hypertension", "hypotension", "ضغط الدم", "ارتفاع الضغط", "انخفاض الضغط"]):
        logging.info("Redirecting to blood pressure search tool.")
        return search_blood_pressure_diseases(query)
    
    # Check for general internet search queries
    if len(words) > 1 or query.isalpha():
        logging.info("Redirecting to general internet search tool.")
        return search_internet(query)
    
    logging.warning("Query did not match any specific tool.")
    return "Query did not match any specific tool."

# Ensure 'loaded_tools' exists before appending
if "loaded_tools" not in globals():
    loaded_tools = []

type(loaded_tools) is list and loaded_tools.append(blood_pressure_tool)
logging.info("BloodPressureSearch tool registered successfully.")
