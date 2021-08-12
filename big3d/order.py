import uuid
import json

from datetime import datetime

from big3d.model import big3D_table
from big3d.utils import validate_incoming_data


def create_new_order(event, context):

    if not event.get("body", None):
        return {"errorCode": 404, "body": "Body not found"}

    data = json.loads(event["body"])

    if not validate_incoming_data(incoming=data, args=["user_id", "order_details"]):
        return {"errorCode": 422, "body": "Order does not have all required attributes"}

    new_order = big3D_table(
        order_id=str(uuid.uuid1()),
        user_id=data.get("user_id"),
        created_at=datetime.utcnow(),
        order_details=json.dumps(data["order_details"]),
    )

    new_order.save()

    return {"statusCode": 200, "body": json.dumps(dict(new_order))}


# SSL Validation Error
def get_user_orders(event, context):
    # I don't know why event['path'] is only returning a string
    results = big3D_table.scan(big3D_table.user_id == event["path"][-36])

    return {"statusCode": 200, "body": json.dumps({"items": [dict(result) for result in results]})}
