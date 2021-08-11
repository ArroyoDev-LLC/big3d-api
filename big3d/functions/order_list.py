import json

from functions.order_model import OrderModel


def order_list(event, context):
    results = OrderModel.scan()

    return {"statusCode": 200, "body": json.dumps({"items": [dict(result) for result in results]})}
