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

Install packages:

```sh
pip install -r requirements.txt
```

[Obtain an API Key](https://www.alphavantage.co/support/#api-key) from AlphaVantage.

Create a ".env" file and add contents like the following (using your own AlphaVantage API Key):

[Obtain credentials from Google Cloud Project OAuth and set them in ".env"]

```sh
# this is the ".env" file:
ALPHAVANTAGE_API_KEY="..."
GOOGLE_CLIENT_ID="..."
GOOGLE_CLIENT_SECRET="..."
GOOGLE_SHEETS_DOCUMENT_ID="..."
```
Further Google Setup:

Upon creating and uploading the Google IDs, go to service accounts, create a service account with the editor permissions, and then create a JSON key that is then uploaded into the root directory and ignored with ".gitignore" for security purposes.

Finally, ensure that the Google Sheets API has been enabled. Create a new sheet, grant it access to the service_client_email in the root-directory json, and then format your sheet accordingly.


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

If CI has been set up, please ensure that your .env variables have been set as repo secrets

```sh
pytest
```