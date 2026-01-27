from langchain_core.tools import tool
import yfinance as yf
import pandas as pd


@tool
def fetch_stock_data(ticker: str, period: str = "1y"):
    """Fetch stock market data for a given ticker symbol.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        period: Time period for historical data (default: '1y')

    Returns:
        Dictionary containing historical price data and company information
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    info = stock.info

    return {
        "historical_data": hist.to_dict(),
        "company_info": info
    }

@tool
def analyze_financials(ticker: str):
    """Analyze financial statements and calculate key ratios for a stock.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')

    Returns:
        Dictionary containing key financial ratios including P/E ratio and Debt-to-Equity
    """
    stock = yf.Ticker(ticker)
    balance_sheet = stock.balance_sheet
    income_stmt = stock.income_stmt
    cash_flow = stock.cashflow
    combined = pd.concat([balance_sheet, income_stmt, cash_flow])

    ratios = {
        "PE Ratio": stock.info.get("trailingPE"), # price-to-earnings
        "Debt to Equity": combined.loc["Total Debt"] / combined.loc["Stockholders Equity"] if "Total Debt" in combined.index and "Stockholders Equity" in combined.index else None,
    }
    return ratios

@tool
def integrate_data(data1: dict, data2: dict):
    """Integrate two datasets by combining them into a single DataFrame.

    Args:
        data1: First dataset as dictionary
        data2: Second dataset as dictionary

    Returns:
        Dictionary containing the integrated combined data
    """
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    integrated = pd.concat([df1, df2], axis=1)
    return integrated.to_dict()

