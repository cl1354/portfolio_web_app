import pandas as pd
import requests
import gspread
import plotly.express as px
from Apps.key_requests import API_KEY
from Apps.key_requests import SHEETS_API_KEY
from Apps.key_requests import SHEETS_KEY

def fetch_sheets_to_pandas(sheets_api_key, sheets_key):
    gc = gspread.api_key(sheets_api_key)
    sh = gc.open_by_key(sheets_key)
    spreadsheet = sh.sheet1.get_all_records(head=1)
    return pd.DataFrame(spreadsheet)

def reformat_date(date_str):
    parts = date_str.split('/')  # Split the date string into parts
    return f"{parts[2]}-{int(parts[0]):02d}-{int(parts[1]):02d}"

df = fetch_sheets_to_pandas(SHEETS_API_KEY,SHEETS_KEY)
df['Date'] = df['Date'].apply(reformat_date)

stocks = [i for i in df['Stock']]

stock_v1 = []

for stock in stocks:
    stock_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={stock}&interval=DAILY&date=2016-01-01&outputsize=full&apikey={API_KEY}'
    stock_r = requests.get(stock_url)
    stock_data = stock_r.json()
    print(stock_data)
    for date, data in stock_data['Time Series (Daily)'].items():
       framework = {'Stock': stock,
                    'Date': date,
                    'Adjusted Close': format_value(data['5. adjusted close'])
                    }
       stock_v1.append(framework)

stock_df = pd.DataFrame(stock_v1)

stock_df.index += 1

filtered_rows = []

# Iterate over rows in df
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

result_df[result_df['Type'] == 'Purchased']

portfolio_value = (
    result_df.groupby('Date')['Total Invested']
    .sum()
    .reset_index()
    .rename(columns={'Total Invested': 'Total Portfolio Value'})
)

print(portfolio_value)
