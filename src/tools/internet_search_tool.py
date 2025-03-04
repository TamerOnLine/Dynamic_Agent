import os
import requests
from bs4 import BeautifulSoup
from langchain.tools import Tool
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("SERPAPI_API_KEY")


def extract_text_from_url(url: str) -> str:
    """Fetches and extracts text content from a webpage."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()  # Raise an error for bad status codes
        
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")  # Extracting paragraphs
        text = "\n".join([p.get_text() for p in paragraphs if p.get_text()])

        return text[:1000] + "..." if len(text) > 1000 else text  # Limit output size
    
    except Exception as e:
        return f"Error extracting text: {e}"


def search_internet(query: str) -> str:
    """Search the internet using SerpAPI and return the top results along with extracted text."""
    if not API_KEY:
        return "API_KEY for SerpAPI is missing. Please check your .env file."

    params = {
        "q": query,
        "api_key": API_KEY,
        "num": 3,  # Fetch top 3 results
        "hl": "en",
    }

    search = GoogleSearch(params)
    results = search.get_dict().get("organic_results", [])

    if not results:
        return "No relevant results found."

    output = []
    for r in results:
        title = r.get("title", "No Title")
        link = r.get("link", "#")
        text_content = extract_text_from_url(link)  # Extract content
        output.append(f"**{title}**\n{link}\n{text_content}\n")

    return "\n".join(output)


# Define the internet search tool
internet_search_tool = Tool(
    name="InternetSearch",
    func=search_internet,
    description="Fetches top search results and extracts text content from webpages.",
    return_direct=True,
)
