import uuid
import json

from datetime import datetime

from big3d.model import Big3D


def create_new_order(event, context):
    data = json.loads(event["body"])

    new_order = Big3D(
        order_id=str(uuid.uuid1()),
        user_id=data.get("user_id"),
        created_at=datetime.utcnow(),
        order_details=json.dumps(data["order_details"]),
    )

    new_order.save()

    return {"statusCode": 201, "body": json.dumps(dict(new_order))}


def get_user_orders(event, context):
    user_id = event["pathParameters"]["user_id"]

    results = Big3D.scan(Big3D.user_id == user_id)

    return {"statusCode": 200, "body": json.dumps({"items": [dict(result) for result in results]})}
