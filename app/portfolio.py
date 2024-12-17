import pandas as pd
from pandas import read_csv
from plotly.express import line
import requests
from app.alpha_service import API_KEY
import gspread

def format_usd(price):
    return f"${float(price):,.2f}"

def format_value(number):
    number = float(number)
    formatted = format(number, '.3f')
    return float(formatted)

def year(date):
    year = date[:4]
    return year

def reformat_date(date_str):
    parts = date_str.split('/')  # Split the date string into parts
    return f"{parts[2]}-{int(parts[0]):02d}-{int(parts[1]):02d}"

# Fetch Google Sheets Data
def fetch_sheets_to_pandas(api_key, sheets_key):
    gc = gspread.api_key(api_key)
    sh = gc.open_by_key(sheets_key)
    spreadsheet = sh.sheet1.get_all_records(head=1)
    return pd.DataFrame(spreadsheet)

# Fetch stock data
def fetch_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}&outputsize=full&datatype=csv"
    return pd.read_csv(url)