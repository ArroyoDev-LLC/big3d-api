import json

from functions.order_model import OrderModel


def order_list(event, context):
    """Returns all orders for a given user"""
    results = OrderModel.scan(OrderModel.user == event["path"]["user_id"])

    return {"statusCode": 200, "body": json.dumps({"items": [dict(result) for result in results]})}
