import pandas as pd
import requests
import gspread
import plotly.express as px
from Apps.key_requests import API_KEY
from Apps.key_requests import SHEETS_API_KEY
from Apps.key_requests import SHEETS_KEY

def fetch_sheets_to_pandas(api_key, sheets_key):
    gc = gspread.api_key(api_key)
    sh = gc.open_by_key(sheets_key)
    spreadsheet = sh.sheet1.get_all_records(head=1)
    return pd.DataFrame(spreadsheet)

