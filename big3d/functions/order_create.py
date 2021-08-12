import json
import uuid

from loguru import logging
from datetime import datetime

from utils import validate_incoming_data
from functions.order_model import OrderModel


def create_order(event, context):
    data = json.loads(event["body"])

    if not validate_incoming_data(
        incoming=data, model_args=["id", "amount", "user_id", "created_at" "order_details"]
    ):
        return {
            "statusCode": 422,
            "body": json.dumps({"error_message": "Order does not contain all valid fields"}),
        }

    new_order = OrderModel(
        id=str(uuid.uuid1()),
        user_id=data["user_id"],
        created_at=datetime.utcnow(),
        order_details=json.dumps(data["details"]),
    )

    new_order.save()

    return {"statusCode": 201, "body": json.dumps(dict(new_order))}
