import json
import uuid

from loguru import logging

from utils import validate_incoming_data
from functions.order_model import OrderModel


def create_order(event, context):
    data = json.loads(event["body"])

    if not validate_incoming_data(incoming=data, model_args=["amount", "user", "details"]):
        return {
            "statusCode": 422,
            "body": json.dumps({"error_message": "Order does not contain all valid fields"}),
        }

    new_order = OrderModel(
        id=str(uuid.uuid1()), user=data["user_id"], details=json.dumps(data["details"])
    )

    new_order.save()

    return {"statusCode": 201, "body": json.dumps(dict(new_order))}
