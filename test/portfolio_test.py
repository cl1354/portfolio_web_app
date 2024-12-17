from app.portfolio import fetch_sheets_to_pandas, fetch_stock_data
import pandas as pd
from app.key_requests import SHEETS_API_KEY, SHEETS_KEY

def test_portfolio():
    portfolio_df = fetch_sheets_to_pandas(SHEETS_API_KEY, SHEETS_KEY)
    assert isinstance(portfolio_df, pd.DataFrame) # Used Google to learn datatype for pandas DataFrame
    assert portfolio_df.columns.tolist() == ["Stock", "Date", "Type", "Quantity"]
    assert len(portfolio_df) != 0

    stock_data = fetch_stock_data("NFLX") # Using a sample stock
    assert isinstance(stock_data, pd.DataFrame) # Used Google to learn datatype for pandas DataFrame
    assert len(stock_data) != 0