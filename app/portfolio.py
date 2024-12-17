import pandas as pd
import requests
from app.key_requests import API_KEY
import gspread

def format_value(number):
    """
    Formatting value but keeping float
    """
    number = float(number)
    formatted = format(number, '.3f')
    return float(formatted)

def reformat_date(date_str):
    """
    Formatting date values into string
    """
    parts = date_str.split('/')  
    return f"{parts[2]}-{int(parts[0]):02d}-{int(parts[1]):02d}"

def fetch_sheets_to_pandas(sheets_api_key, sheets_key):
    """
    Fetching info from google sheets and transforming it into a dataframe
    """
    gc = gspread.api_key(sheets_api_key)
    sh = gc.open_by_key(sheets_key)
    spreadsheet = sh.sheet1.get_all_records(head=1)
    return pd.DataFrame(spreadsheet)


def fetch_stock_data(symbol):
    """
    Fetching stock data from Alphavantage
    """
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}&outputsize=full&datatype=csv"
    return pd.read_csv(url)