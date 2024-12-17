from flask import Blueprint, request, render_template, redirect, flash

from app.portfolio import format_usd, format_value, year, reformat_date, build_stock_list, build_returns_df

portfolio_routes = Blueprint("portfolio_routes", __name__)

#REPLACE
symbol = "NFLX"

@portfolio_routes.route("/")
def portfolio_dashboard():
    print("Portfolio Dashboard")
    try:
        df = build_returns_df(build_stock_list("NFLX"))
        return render_template("portfolio.html")
    except Exception as err:
        print("Oops!", err)
        flash("Error. Please try again!", "danger")
        return redirect("/")

# Charles you need to remove all stocks routing references and do portfolio references instead

    # try:
    #     df = fetch_stocks_csv(symbol=symbol)
    #     latest_close_usd = format_usd(df.iloc[0]["adjusted_close"])
    #     latest_date = df.iloc[0]["timestamp"]
    #     data = df.to_dict("records")
    #     flash("Fetched Real-time Market Data!", "success")
    #     return render_template("portfolio_dashboard.html",
    #         symbol=symbol,
    #         latest_close_usd=latest_close_usd,
    #         latest_date=latest_date,
    #         data=data
    #     )

# API ROUTES