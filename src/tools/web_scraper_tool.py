import logging
import requests
from bs4 import BeautifulSoup
from langchain.tools import Tool

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scrape_webpage(url: str) -> str:
    """
    Extracts and returns the main text content from a webpage.
    """
    logging.info(f"Scraping webpage: {url}")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        logging.info("Successfully fetched webpage content.")

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text_content = "\n".join([p.get_text() for p in paragraphs if p.get_text()])

        logging.info("Successfully extracted text from webpage.")
        return text_content[:5000] + "..." if len(text_content) > 5000 else text_content
    
    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP error while scraping webpage: {e}")
        return f"Error scraping the webpage: {e}"
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return f"Error scraping the webpage: {e}"

# Define the tool in LangChain
web_scraper_tool = Tool(
    name="WebScraper",
    func=scrape_webpage,
    description="Scrapes webpage content and extracts text data.",
    return_direct=True,
)

# Ensure 'loaded_tools' exists before appending
if "loaded_tools" not in globals():
    loaded_tools = []

type(loaded_tools) is list and loaded_tools.append(web_scraper_tool)
logging.info("WebScraper tool registered successfully.")
