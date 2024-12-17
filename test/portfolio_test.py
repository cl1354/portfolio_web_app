from app.portfolio import build_stock_list, build_returns_df
import pandas as pd

def test_portfolio():
    built_stock_list = build_stock_list("NFLX")
    assert isinstance(built_stock_list, list)
    for entry in built_stock_list:
        assert list(entry.keys()) == ["Stock", "Date", "Adjusted Close"] # Used Google to learn how to make list of keys

    built_returns_df = build_returns_df(built_stock_list)
    assert isinstance(built_returns_df, pd.DataFrame) # Used Google to learn datatype for pandas DataFrame

    columns = built_returns_df.columns.tolist()
    assert columns == ["Date", "Total Portfolio Value", "Return"]