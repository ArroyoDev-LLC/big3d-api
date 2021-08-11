import json

from pynamodb.exceptions import DoesNotExist
from functions.order_model import OrderModel


def get(event, context):
    try:
        found_order = OrderModel.get(hash_key=event["path"]["id"])
    except:
        return {"statusCode": 404, "body": json.dumps({"error_message": "Order not found"})}

    return {"status_code": 200, "body": json.dumps(dict(found_order))}
