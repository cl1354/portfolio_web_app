from flask import Blueprint, request, render_template
import requests
import pandas as pd
import plotly.express as px
from app.portfolio import format_value, reformat_date
from app.key_requests import SHEETS_API_KEY
from app.key_requests import SHEETS_KEY
from app.key_requests import API_KEY
from app.portfolio import fetch_sheets_to_pandas, fetch_stock_data

portfolio_routes = Blueprint("portfolio_routes", __name__)

# Configure Routes
@portfolio_routes.route("/", methods=["GET", "POST"])
def configure_routes():
    # Fetch data from Google Sheets
    df = fetch_sheets_to_pandas(SHEETS_API_KEY, SHEETS_KEY)
    df['Date'] = df['Date'].apply(reformat_date)
    # Default date range
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    start_date = request.form.get("start_date", min_date)
    end_date = request.form.get("end_date", max_date)
    # Fetch stock data
    stocks = df['Stock'].unique()
    stock_v1 = []
    for stock in stocks:
        stock_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={stock}&outputsize=full&apikey={API_KEY}'
        stock_r = requests.get(stock_url)
        stock_data = stock_r.json()
        for date, data in stock_data['Time Series (Daily)'].items():
            stock_v1.append({
                'Stock': stock,
                'Date': date,
                'Adjusted Close': format_value(data['5. adjusted close'])
            })
    stock_df = pd.DataFrame(stock_v1)
    stock_df.index += 1
    # Filter rows and calculate
    filtered_rows = []
    for _, row in df.iterrows():
        stock, date = row['Stock'], row['Date']
        # Filter stock_df
        filtered_stock_data = stock_df[stock_df['Stock'] == stock].copy()
        # Add 'Type' column, want to make sure we keep track of when it's purchased
        filtered_stock_data['Type'] = filtered_stock_data['Date'].apply(
            lambda x: "Purchased" if x == date else "Hold" if x > date else "Pre-Purchase"
        )
        # Set Total Invested: 0 for Pre-Purchase dates
        filtered_stock_data['Quantity'] = row['Quantity']
        filtered_stock_data['Total Invested'] = filtered_stock_data.apply(
            lambda x: 0 if x['Type'] == "Pre-Purchase" else x['Quantity'] * x['Adjusted Close'], axis=1
        )
        filtered_rows.append(filtered_stock_data)

    result_df = pd.concat(filtered_rows, ignore_index=True)
    result_df = result_df[(result_df['Date'] >= start_date) & (result_df['Date'] <= end_date)]

    # Choice to choose show portfolio value or individual stock values
    show_total = request.form.get("show_total", "false").lower() == "true"
    if show_total:
        # Aggregate to show total portfolio value
        portfolio_value = (
            result_df.groupby('Date')['Total Invested']
            .sum()
            .reset_index()
            .rename(columns={'Total Invested': 'Total Portfolio Value'})
        )
        # Plot total portfolio value
        fig = px.line(
            portfolio_value,
            x="Date",
            y="Total Portfolio Value",
            title="Total Portfolio Value Over Time",
            template="plotly_dark"
        )
        y_label = "Total Portfolio Value ($)"
    else:
        # Show individual stock values using filtered_rows
        individual_stock_values = result_df.groupby(['Date', 'Stock'])['Total Invested'].sum().reset_index()
        fig = px.line(
            individual_stock_values,
            x="Date",
            y="Total Invested",
            color="Stock",
            title="Individual Stock Values Over Time",
            template="plotly_dark"
        )
        y_label = "Total Invested ($)"
    fig.update_layout(xaxis_title="Date", yaxis_title=y_label)
    plot_html = fig.to_html(full_html=False)

    return render_template(
        "portfolio.html",
        plot=plot_html,
        start_date=start_date,
        end_date=end_date,
        show_total=show_total
    )