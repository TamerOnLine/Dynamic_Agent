import sqlite3
import datetime

from tools.weather_tool import weather_tool
from tools.stock_tool import stock_tool
from tools.custom_tool import custom_tool
from tools.internet_search_tool import internet_search_tool
from tools.blood_pressure_tool import blood_pressure_tool 
from tools.web_scraper_tool import web_scraper_tool
from tools.advanced_web_scraper import advanced_web_scraper


from model.ollama_model import OllamaHandler
from langchain.agents import initialize_agent, AgentType


class Agent:
    """AI agent integrating weather, stock, blood pressure, and other tools using LangChain."""

    def __init__(self):
        """Initialize the AI agent with tools."""
        self.handler = OllamaHandler()
        self.tools = [
            weather_tool,
            stock_tool,
            custom_tool,
            internet_search_tool,
            blood_pressure_tool,
            web_scraper_tool,
            advanced_web_scraper,
        ]

        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.handler.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            allowed_tools=[
                "Use the Weather API",
                "StockPrice",
                "GeneralResponse",
                "InternetSearch",
                "BloodPressureSearch",
                "WebScraper",
                "AdvancedWebScraper"
            ],
            handle_parsing_errors=True,
        )

        # Create SQLite database if it does not exist
        self.init_db()

    def init_db(self):
        """Create a table to store questions, answers, and tool used."""
        with sqlite3.connect("chat_history.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    question TEXT,
                    answer TEXT,
                    tool_used TEXT
                )
                """
            )
            conn.commit()

    def log_interaction(self, query, response, tool_used):
        """Log questions, answers, and tool used in the database."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect("chat_history.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO chat_log (timestamp, question, answer, tool_used) VALUES (?, ?, ?, ?)",
                (timestamp, query, response, tool_used),
            )
            conn.commit()

    def process(self, query):
        """
        Pass the query to the agent to determine the appropriate tool.

        Args:
            query (str): User query.

        Returns:
            str: The agent's response.
        """
        try:
            result = self.agent.invoke(query)
            response = result.get("output", "No response")
            
            # Debugging: Print full result to analyze structure
            print("Full Agent Response:", result)
            
            # Extract tool used from the agent's response structure
            tool_used = "Unknown"
            thought_text = result.get("thought", "")
            print(f"Processed Thought Text: {thought_text}")  # Debugging log
            
            if "Action:" in thought_text:
                thought_lines = thought_text.split("\n")
                for line in thought_lines:
                    if "Action:" in line:
                        tool_used = line.replace("Action:", "").strip()
                        break
            
            print(f"Extracted Tool Used: {tool_used}")  # Debugging log
            
            self.log_interaction(query, response, tool_used)  # Log the interaction
            return response
        except Exception as e:
            print(f"Error processing query: {e}")
            return "An error occurred while processing your request."
