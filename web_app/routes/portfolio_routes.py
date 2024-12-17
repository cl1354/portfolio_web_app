from flask import Blueprint, request, render_template
import pandas as pd
import gspread
import plotly.express as px
from app.key_requests import API_KEY
from app.key_requests import SHEETS_API_KEY
from app.key_requests import SHEETS_KEY
from app.portfolio import fetch_sheets_to_pandas, fetch_stock_data

portfolio_routes = Blueprint("portfolio_routes", __name__)

# Configure Routes
@portfolio_routes.route("/", methods=["GET", "POST"])
def create_dashboard():
    # Default values for date range and view mode
    start_date = request.form.get("start_date", "2023-01-01")
    end_date = request.form.get("end_date", "2024-01-01")
    show_total = request.form.get("show_total", "false").lower() == "true"

    # Fetch Google Sheets Data
    df = fetch_sheets_to_pandas(SHEETS_API_KEY, SHEETS_KEY)
    stocks = df['Stock'].unique()

    # Fetch stock data
    stock_data = []
    for stock in stocks:
        data = fetch_stock_data(stock)
        data["Stock"] = stock
        stock_data.append(data)

    combined_df = pd.concat(stock_data)
    combined_df = combined_df[["timestamp", "adjusted_close", "Stock"]]
    combined_df.columns = ["Date", "Adjusted Close", "Stock"]
    combined_df["Date"] = pd.to_datetime(combined_df["Date"])

    # Filter data based on user-specified date range
    mask = (combined_df["Date"] >= pd.to_datetime(start_date)) & (combined_df["Date"] <= pd.to_datetime(end_date))
    filtered_df = combined_df[mask]

    # Plot: Total Portfolio Value or Individual Stock Values
    if show_total:
        portfolio_value = filtered_df.groupby("Date")["Adjusted Close"].sum().reset_index()
        fig = px.line(portfolio_value, x="Date", y="Adjusted Close", title="Total Portfolio Value Over Time")
        fig.update_layout(template="plotly_dark", xaxis_title="Date", yaxis_title="Total Value ($)")
    else:
        fig = px.line(filtered_df, x="Date", y="Adjusted Close", color="Stock",
                        title="Individual Stock Values Over Time")
        fig.update_layout(template="plotly_dark", xaxis_title="Date", yaxis_title="Stock Value ($)")

    # Convert the plot to HTML
    plot_html = fig.to_html(full_html=False)

    return render_template("portfolio.html", plot=plot_html, start_date=start_date, end_date=end_date, show_total=show_total)
    