# portfolio_web_app

## Setup

Create a virtual environment (first time only):

```sh
conda create -n port-viz python=3.10
```

Activate the environment (whenever you come back to this project):

```sh
conda activate port-viz
```

Install package depdencies stored in requirements.txt:

```sh
pip install -r requirements.txt
```

[Obtain an API Key](https://www.alphavantage.co/support/#api-key) from AlphaVantage.

Create a ".env" file and add contents like the following (using your own AlphaVantage API Key):

[Obtain credentials from 'gspread'](https://docs.gspread.org/en/latest/oauth2.html#enable-api-access)
from Google Developer. This is to be used with public worksheets for the simplified purpose of the webapp

```sh
# this is the ".env" file:
ALPHAVANTAGE_API_KEY="..."
SHEETS_API_KEY="..."
SHEETS_KEY="..."
```

Run the web app (then view in the browser at http://localhost:5000/):
```sh
# Mac OS:
FLASK_APP=web_app flask run

# Windows OS:
# ... if `export` doesn't work for you, try `set` instead
# ... or set FLASK_APP variable via ".env" file
export FLASK_APP=web_app
flask run
```

Testing:

If CI has been set up, please ensure that your .env variables have been set as repo secrets.
If you manually, wish to run tests throughout modification of the code, please run the below command:

```sh
pytest
```