import os
from langchain.tools import Tool
from serpapi import GoogleSearch
from dotenv import load_dotenv
from tools.internet_search_tool import search_internet  # استيراد البحث العام

# Load environment variables
load_dotenv()

# Retrieve SerpAPI API key from environment variables
API_KEY = os.getenv("SERPAPI_API_KEY")

def search_blood_pressure_diseases(query: str) -> str:
    """Search the internet for blood pressure-related diseases using SerpAPI."""
    if not API_KEY:
        return "API_KEY for SerpAPI is missing. Please check your .env file."

    params = {
        "q": f"{query} blood pressure disease",
        "api_key": API_KEY,
        "num": 5,
        "hl": "en",
    }

    search = GoogleSearch(params)
    results = search.get_dict().get("organic_results", [])

    if not results:
        return "No relevant results found."

    return "\n".join([f"{r['title']}: {r['link']}" for r in results]) + "\n"

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
    words = query_lower.split()

    # Check for blood pressure disease queries
    if any(keyword in query_lower for keyword in ["blood pressure", "hypertension", "hypotension", "ضغط الدم", "ارتفاع الضغط", "انخفاض الضغط"]):
        return search_blood_pressure_diseases(query)
    
    # Check for general internet search queries
    if len(words) > 1 or query.isalpha():
        return search_internet(query)  # تم إصلاح الخطأ بإضافة الاستيراد الصحيح
    
    return "Query did not match any specific tool."