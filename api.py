import datetime
import os
import uuid
import re
from flask import Flask, request, jsonify
from flask_expects_json import expects_json
from schema import ReceiptSchema
from math import ceil

app = Flask(__name__)

# would maybe set up a cache or something better here even though not required
receipts = {}

@app.route("/receipts/process", methods=["POST"])
@expects_json(ReceiptSchema)
def process():
    receipt = request.get_json()
    # was going to just have an increment counter but this felt safer
    receipt_id = str(uuid.uuid4())

    try:
        # get points and assign back to the receipt
        receipt["points"] = receipt_points(receipt)
    except Exception as e:
        return {
            "ERROR": "Receipt Processing Error",
            "MESSAGE": e.message,
        }, 400
    
    receipts[receipt_id] = receipt
    return {"id": receipt_id}, 200


@app.route("/receipts/{id}/points", methods=["GET"])
def get_points(receipt_id):
    # return points from receipt field
    try:
        return {"points": receipts[receipt_id]["points"]}
    except Exception as e:
        return {
            "ERROR": "Point Getting Error",
            "MESSAGE": e.message,
        }, 400


def receipt_points(receipt):
    total = 0
    # regex for alphanumerics; apparently faster than alnum
    total += len(re.sub(r'\W+', '', receipt["retailer"]))

    dollar_amount = float(receipt["total"])
    # check if dollar amount is round or is mult of 25
    if dollar_amount.is_integer():
        total += 50
    elif dollar_amount % 0.25 == 0:
        total += 25

    # points for item count
    total += 5*(len(receipt["items"])//2)

    # trimmed item descriptions mult of 3 check
    for item in receipt["items"]:
        if len(item["shortDescription"].strip()) % 3 == 0:
            points_total += ceil(float(item["price"])*0.2)

    # odd day check (could be changed to relative to 365)
    date = datetime.date(receipt["purchaseDate"])
    if date.day % 2 == 0:
        total += 6

    # time of purchase between 2 and 4pm (local)
    time = datetime.time(receipt["purchaseTime"])
    if time > datetime.time(hours=14,minutes=0) and time < datetime.time(hours=16,minutes=0):
        total += 10

    
    return total



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(debug=False, host="0.0.0.0", port=port)