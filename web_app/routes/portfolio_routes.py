from flask import Blueprint, request, render_template, redirect, flash

from app.portfolio import fetch_stocks_csv, format_usd

portfolio_routes = Blueprint("portfolio_routes", __name__)

@portfolio_routes.route("/portfolio/form")
def portfolio_form():
    print("PORTFOLIO FORM...")
    return render_template("portfolio_form.html")
@portfolio_routes.route("/portfolio/dashboard", methods=["GET", "POST"])
def portfolio_dashboard():
    print("PORTFOLIO DASHBOARD...")
    if request.method == "POST":
        # for data sent via POST request, form inputs are in request.form:
        request_data = dict(request.form)
        print("FORM DATA:", request_data)
    else:
        # for data sent via GET request, url params are in request.args
        request_data = dict(request.args)
        print("URL PARAMS:", request_data)

    symbol = request_data.get("symbol") or "NFLX" # get specific symbol or use default NFLX

# Charles you need to remove all stocks routing references and do portfolio references instead

    try:
        df = fetch_stocks_csv(symbol=symbol)
        latest_close_usd = format_usd(df.iloc[0]["adjusted_close"])
        latest_date = df.iloc[0]["timestamp"]
        data = df.to_dict("records")
        flash("Fetched Real-time Market Data!", "success")
        return render_template("portfolio_dashboard.html",
            symbol=symbol,
            latest_close_usd=latest_close_usd,
            latest_date=latest_date,
            data=data
        )
    except Exception as err:
        print('OOPS', err)
        flash("Market Data Error. Please check your symbol and try again!", "danger")
        return redirect("/portfolio/form")
#
# API ROUTES
#
@portfolio_routes.route("/api/portfolio.json")
def portfolio_api():
    print("PORTFOLIO DATA (API)...")
    # for data supplied via GET request, url params are in request.args:
    url_params = dict(request.args)
    print("URL PARAMS:", url_params)
    symbol = url_params.get("symbol") or "NFLX"
    try:
        df = fetch_stocks_csv(symbol=symbol)
        data = df.to_dict("records") # convert dataframe to list of dict
        return {"symbol": symbol, "data": data}
    except Exception as err:
        print('OOPS', err)
        return {"message":"Market Data Error. Please try again."}, 404   