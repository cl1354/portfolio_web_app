from flask import Flask

from web_app.routes.portfolio_routes import portfolio_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(portfolio_routes)
    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)