
import yfinance as yf

from langchain.tools import Tool


import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="langchain")


def get_stock_price(ticker: str):
    """
    Fetch the current closing price of a given stock using Yahoo Finance.
    
    :param ticker: The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    :return: The current stock price or an error message.
    """
    ticker = ticker.strip().upper().replace("'", "").replace('"', "")

    stock = yf.Ticker(ticker)

    if stock.info.get("regularMarketPrice") is None:
        return f" Stock {ticker} is unavailable or might have been removed from Yahoo Finance."

    history = stock.history(period="1d")

    if history.empty:
        return f" No available data for {ticker}. The market might be closed or insufficient data exists."

    price = history["Close"].iloc[-1]
    return f"The current price of {ticker} is {price:.2f} USD."


# Create a tool within LangChain using `get_stock_price`
stock_tool = Tool(
    name="StockPrice",
    func=get_stock_price,
    description="Fetches the current stock price using Yahoo Finance.",
    return_direct=True
)


