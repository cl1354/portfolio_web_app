# LOCAL DEV (ENV VARS)

from pandas import read_csv
from plotly.express import line


from app.alpha_service import API_KEY


def format_usd(my_price):
    return f"${float(my_price):,.2f}"

def format_value(number):
    number = float(number)
    formatted = format(number, '.3f')
    return float(formatted)

def year(date):
    year = date[:4]
    return year

def fetch_stocks_csv(symbol):
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}&outputsize=full&datatype=csv"
    df = read_csv(request_url)
    return df


if __name__ == "__main__":

    # SELECT A SYMBOL

    symbol = input("Please input a symbol (e.g. 'NFLX'): ") or "NFLX"
    print("SYMBOL:", symbol)

    # FETCH THE DATA

    df = fetch_stocks_csv(symbol)

    print(df.columns)
    print(len(df))
    print(df.head())
