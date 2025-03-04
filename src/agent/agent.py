import sqlite3
import datetime
import logging

from model.ollama_model import OllamaHandler
from langchain.agents import initialize_agent, AgentType


class Agent:
    """Intelligent agent utilizing multiple tools via LangChain."""

    def __init__(self, tools=None):
        """Initialize the agent with optional dynamic tools."""
        self.handler = OllamaHandler()
        self.tools = tools if tools else []

        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.handler.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            allowed_tools=[tool.name for tool in self.tools],
            handle_parsing_errors=True,
        )

        # Initialize the database
        self.init_db()

    def init_db(self):
        """Create necessary tables in the database if they do not exist."""
        with sqlite3.connect("chat_history.db") as conn:
            cursor = conn.cursor()

            # Tools table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tools (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT
                )
                """
            )

            # Chat log table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    question TEXT,
                    answer TEXT,
                    tool_id INTEGER,
                    FOREIGN KEY (tool_id) REFERENCES tools(id)
                )
                """
            )

            # Error log table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS error_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    error_message TEXT,
                    query TEXT,
                    tool_id INTEGER,
                    FOREIGN KEY (tool_id) REFERENCES tools(id)
                )
                """
            )

            conn.commit()

    def log_interaction(self, query, response, tool_name):
        """Log conversations with tool identification."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect("chat_history.db") as conn:
            cursor = conn.cursor()

            # Retrieve or insert tool_id
            cursor.execute("SELECT id FROM tools WHERE name = ?", (tool_name,))
            tool_id = cursor.fetchone()

            if tool_id is None:
                cursor.execute("INSERT INTO tools (name, description) VALUES (?, ?)",
                               (tool_name, "Undefined description"))
                tool_id = cursor.lastrowid
            else:
                tool_id = tool_id[0]

            # Log the conversation
            cursor.execute(
                "INSERT INTO chat_log (timestamp, question, answer, tool_id) VALUES (?, ?, ?, ?)",
                (timestamp, query, response, tool_id),
            )
            conn.commit()

    def log_error(self, query, error_message, tool_name=None):
        """Log errors occurring during processing."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect("chat_history.db") as conn:
            cursor = conn.cursor()

            # Retrieve tool_id if error is related to a specific tool
            tool_id = None
            if tool_name:
                cursor.execute("SELECT id FROM tools WHERE name = ?", (tool_name,))
                tool_id = cursor.fetchone()
                if tool_id:
                    tool_id = tool_id[0]

            # Insert error log
            cursor.execute(
                "INSERT INTO error_log (timestamp, error_message, query, tool_id) VALUES (?, ?, ?, ?)",
                (timestamp, error_message, query, tool_id),
            )
            conn.commit()

    def process(self, query):
        """
        Pass the query to the agent to determine the appropriate tool.

        Args:
            query (str): User query.

        Returns:
            str: Agent response.
        """
        try:
            result = self.agent.invoke(query)
            response = result.get("output", "No response")

            # Extract the tool used
            tool_used = "Unknown"
            thought_text = result.get("thought", "")

            if "Action:" in thought_text:
                thought_lines = thought_text.split("\n")
                for line in thought_lines:
                    if "Action:" in line:
                        tool_used = line.replace("Action:", "").strip()
                        break

            self.log_interaction(query, response, tool_used)
            return response

        except Exception as e:
            error_message = str(e)
            self.log_error(query, error_message)
            logging.error(f"Error processing query: {error_message}")
            return "An error occurred while processing your request. Please try again later."
