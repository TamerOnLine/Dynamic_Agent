import os
import requests
import logging
from dotenv import load_dotenv
from langchain.tools import Tool

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_weather(city: str) -> str:
    """Fetch weather information for a given city."""
    if not API_KEY:
        logging.error("API_KEY is missing. Please check the .env file.")
        return "API_KEY is missing. Please check the .env file."

    url = (
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    )
    logging.info(f"Fetching weather data for city: {city}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if "weather" in data and "main" in data:
            weather_desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            logging.info(f"Weather data retrieved successfully for {city}.")
            return f"Weather in {city}: {weather_desc}, Temperature: {temp}°C."
        
        logging.warning(f"Unexpected response format: {data}")
        return "An error occurred while fetching data."
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
        return "Failed to retrieve weather data."

# Define the weather tool
weather_tool = Tool(
    name="WeatherTool",
    func=get_weather,
    description="Fetches weather information for a given city.",
    return_direct=True,
)

# Ensure 'loaded_tools' exists before appending
if "loaded_tools" not in globals():
    loaded_tools = []

type(loaded_tools) is list and loaded_tools.append(weather_tool)
logging.info("WeatherTool registered successfully.")
