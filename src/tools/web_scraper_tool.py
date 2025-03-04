import requests
from bs4 import BeautifulSoup
from langchain.tools import Tool

def scrape_webpage(url: str) -> str:
    """
    Extracts and returns the main text content from a webpage.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text_content = "\n".join([p.get_text() for p in paragraphs if p.get_text()])

        return text_content[:5000] + "..." if len(text_content) > 5000 else text_content
    
    except Exception as e:
        return f"Error scraping the webpage: {e}"

# تعريف الأداة في LangChain
web_scraper_tool = Tool(
    name="WebScraper",
    func=scrape_webpage,
    description="Scrapes webpage content and extracts text data.",
    return_direct=True,
)
