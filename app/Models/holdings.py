from pprint import pprint

from app.db import BaseModel

class Holding(BaseModel):

    SHEET_NAME = "holdings"

    COLUMNS = ["Stock", "Date", "Type", "Quantity"]

    SEEDS= []

if __name__ == "__main__":

    holdings = Holding.all()
    print("FOUND", len(orders), "ORDERS")
    for holding in holdings:
        pprint(dict(holding))