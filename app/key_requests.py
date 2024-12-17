import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="demo")
SHEETS_API_KEY = os.getenv("SHEETS_API_KEY", default="demo")
SHEETS_KEY = os.getenv("SHEETS_KEY", default="demo")