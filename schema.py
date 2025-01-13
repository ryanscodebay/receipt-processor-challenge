from apischema import Schema

class ReceiptSchema(Schema):
    "type": "object"
    "properties"= {
        "retailer": {"type": "string"},
        "purchaseDate": {"type": "string"},
        "purchaseTime": {"type": "string"},
        "total": {"type": "string"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "shortDescription": {"type": "string"},
                    "price": {"type": "string"},
                },
            },
        },
    }