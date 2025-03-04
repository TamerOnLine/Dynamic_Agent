# AI Agent with LangChain and Ollama

## Overview
This project is an AI-powered agent built using **LangChain**, integrating **Ollama** for natural language processing and automation. It allows users to retrieve **weather information**, **stock prices**, and **engage in general conversations** through an intelligent query system.

## Features
- **Weather Forecasting**: Fetches live weather updates using OpenWeather API.
- **Stock Price Retrieval**: Retrieves stock market data via Yahoo Finance.
- **General Query Handling**: If no specific tool matches the query, an AI chatbot (Ollama) responds dynamically.
- **Error Handling & Logging**: Ensures a robust system with proper logging and exception handling.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- `pip` (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai-agent.git
   cd ai-agent
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your OpenWeather API key:
   ```env
   API_KEY=your_openweather_api_key
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## File Structure
```
├── agent.py           # AI agent with LangChain integration
├── main.py            # Entry point of the application
├── weather_tool.py    # Weather retrieval module
├── stock_tool.py      # Stock price retrieval module
├── custom_tool.py     # General query processing tool
├── ollama_model.py    # Ollama model wrapper
├── requirements.txt   # List of dependencies
└── .env               # Environment variables (not included in repo)
```

## Usage
- The system prompts users with:
  ```bash
  Ask about the weather or stock prices (or type 'exit' to quit):
  ```
- Example queries:
  ```bash
  What's the weather in Berlin?
  ```
  ```bash
  What is the stock price of AAPL?
  ```
- If no specific tool matches the query, the AI assistant provides a response dynamically.

## Technologies Used
- **LangChain**: For AI agent workflow.
- **Ollama**: AI model for query processing.
- **OpenWeather API**: Weather data.
- **Yahoo Finance (yfinance)**: Stock price retrieval.
- **Python-dotenv**: For environment variable management.
- **Requests**: For making API calls.

## Future Enhancements
- **Add GUI for better user interaction**
- **Support more APIs (e.g., news, cryptocurrency)**
- **Enhance stock price analysis with historical trends**

## License
MIT License. Feel free to contribute and improve!

## Author
Developed by **Tamer Hamad Faour**.

---
🚀 Feel free to fork, improve, and suggest enhancements!

