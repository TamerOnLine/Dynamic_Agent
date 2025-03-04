import yfinance as yf
import logging
from langchain.tools import Tool
import warnings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module="langchain")

def get_stock_price(ticker: str):
    """
    Fetch the current closing price of a given stock using Yahoo Finance.
    
    :param ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    :return: The current stock price or an error message.
    """
    ticker = ticker.strip().upper().replace("'", "").replace('"', "")
    logging.info(f"Fetching stock data for: {ticker}")
    
    stock = yf.Ticker(ticker)
    
    if stock.info.get("regularMarketPrice") is None:
        logging.error(f"Stock {ticker} is unavailable or removed from Yahoo Finance.")
        return f"Stock {ticker} is unavailable or might have been removed from Yahoo Finance."
    
    history = stock.history(period="1d")
    
    if history.empty:
        logging.warning(f"No available data for {ticker}. Market might be closed.")
        return f"No available data for {ticker}. The market might be closed or insufficient data exists."
    
    price = history["Close"].iloc[-1]
    logging.info(f"Stock data retrieved successfully for {ticker}. Price: {price:.2f} USD")
    return f"The current price of {ticker} is {price:.2f} USD."

# Create a tool within LangChain using `get_stock_price`
stock_tool = Tool(
    name="StockPrice",
    func=get_stock_price,
    description="Fetches the current stock price using Yahoo Finance.",
    return_direct=True
)

# Ensure 'loaded_tools' exists before appending
if "loaded_tools" not in globals():
    loaded_tools = []

type(loaded_tools) is list and loaded_tools.append(stock_tool)
logging.info("StockPrice tool registered successfully.")
