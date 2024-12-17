from flask import Flask
from web_app.routes.stock_routes import configure_routes

app = Flask(__name__)

# Register routes from routes folder
configure_routes(app)

if __name__ == "__main__":
    app.run(debug=True) 