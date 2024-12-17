import pandas as pd
from pandas import read_csv
from plotly.express import line
import requests
from app.alpha_service import API_KEY

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

def build_stock_list(stock):
    stock_v2 = []
    stock_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={stock}&interval=DAILY&date=2016-01-01&outputsize=full&apikey={API_KEY}"
    stock_r = requests.get(stock_url)
    stock_data = stock_r.json()
    for date, data in stock_data['Time Series (Daily)'].items():
        framework = {
            'Stock': stock,
            'Date': date,
            'Adjusted Close': format_value(data['5. adjusted close'])
            }
        stock_v2.append(framework)
    return stock_v2

def build_returns_df(stock_v1):
    stock_df = pd.DataFrame(stock_v1)
    stock_df.index += 1

    filtered_rows = []

    for _, row in df.iterrows():
        stock = row['Stock']
        date = row['Date']

        # Filter stock_df for the same stock and dates after or equal to the given date
        filtered_stock_data = stock_df[(stock_df['Stock'] == stock) & (stock_df['Date'] >= date)].copy()

        # Determine 'Type' column and update values
        filtered_stock_data['Type'] = filtered_stock_data['Date'].apply(
            lambda x: "Purchased" if x == date else "Hold"
        )

        # Set 'Quantity' and calculate 'Total Invested'
        filtered_stock_data['Quantity'] = row['Quantity']
        filtered_stock_data['Total Invested'] = filtered_stock_data['Quantity'] * filtered_stock_data['Adjusted Close']

        # Append the filtered rows to the result
        filtered_rows.append(filtered_stock_data)

    # Concatenate the filtered results into a single DataFrame
    result_df = pd.concat(filtered_rows, ignore_index=True)

    # Display the result
    print(result_df)

    result_df[result_df['Type'] == 'Purchased']

    portfolio_value = (
        result_df.groupby('Date')['Total Invested']
        .sum()
        .reset_index()
        .rename(columns={'Total Invested': 'Total Portfolio Value'})
    )

    portfolio_value['Return'] = portfolio_value['Total Portfolio Value'].pct_change()*100

    return portfolio_value


# def fetch_stocks_csv(symbol):
#     request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={API_KEY}&outputsize=full&datatype=csv"
#     df = read_csv(request_url)
#     return df

# if __name__ == "__main__":

DOCUMENT_ID = "19tdtumbB1l4gr4HE1V36UnNFtb0LdfXVBq5PugWnFHM"
SHEET_NAME = "Sheet1"

rows = [
    {'Stock': 'NVDA', 'Date': '10/2/2023', 'Type': 'Buy', 'Quantity': 1},
    {'Stock': 'COST', 'Date': '10/4/2023', 'Type': 'Buy', 'Quantity': 2},
    {'Stock': 'VOO', 'Date': '10/5/2023', 'Type': 'Buy', 'Quantity': 1}
    ]

df = pd.DataFrame(rows)
df['Date'] = df['Date'].apply(reformat_date)

stocks = [i for i in df['Stock']]

stock_v1 = []

for stock in stocks:
    stock_framework = build_stock_list(stock)
    stock_v1 += stock_framework

portfolio_value = build_returns_df(stock_v1)

print(portfolio_value)