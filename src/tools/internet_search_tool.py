import os
import logging
import requests
from bs4 import BeautifulSoup
from langchain.tools import Tool
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
API_KEY = os.getenv("SERPAPI_API_KEY")

def extract_text_from_url(url: str) -> str:
    """Fetches and extracts text content from a webpage."""
    logging.info(f"Extracting text from URL: {url}")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()  # Raise an error for bad status codes
        
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")  # Extracting paragraphs
        text = "\n".join([p.get_text() for p in paragraphs if p.get_text()])
        
        logging.info("Successfully extracted text from webpage.")
        return text[:1000] + "..." if len(text) > 1000 else text  # Limit output size
    except Exception as e:
        logging.error(f"Error extracting text: {e}")
        return f"Error extracting text: {e}"

def search_internet(query: str) -> str:
    """Search the internet using SerpAPI and return the top results along with extracted text."""
    if not API_KEY:
        logging.error("API_KEY for SerpAPI is missing. Please check your .env file.")
        return "API_KEY for SerpAPI is missing. Please check your .env file."
    
    logging.info(f"Searching internet for query: {query}")
    params = {
        "q": query,
        "api_key": API_KEY,
        "num": 3,  # Fetch top 3 results
        "hl": "en",
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict().get("organic_results", [])
        
        if not results:
            logging.warning("No relevant results found.")
            return "No relevant results found."
        
        output = []
        for r in results:
            title = r.get("title", "No Title")
            link = r.get("link", "#")
            logging.info(f"Fetching content from: {link}")
            text_content = extract_text_from_url(link)  # Extract content
            output.append(f"**{title}**\n{link}\n{text_content}\n")
        
        logging.info("Internet search completed successfully.")
        return "\n".join(output)
    except Exception as e:
        logging.error(f"Error during internet search: {e}")
        return "An error occurred during internet search."

# Define the internet search tool
internet_search_tool = Tool(
    name="InternetSearch",
    func=search_internet,
    description="Fetches top search results and extracts text content from webpages.",
    return_direct=True,
)

# Ensure 'loaded_tools' exists before appending
if "loaded_tools" not in globals():
    loaded_tools = []

type(loaded_tools) is list and loaded_tools.append(internet_search_tool)
logging.info("InternetSearch tool registered successfully.")
