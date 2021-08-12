import uuid

from model import big3D_table
from big3d.utils import validate_incoming_data

def create_new_order(event, context):
    data = json.loads(event['body'])

    if not validate_incoming_data(incoming=data, args["user_id", "order_details"]):
        return {"errorCode" : 422, "body" : "Order does not have all required attributes"}

    new_order = big3D_table(order_id=str(uuid.uuid1()),
                 user_id=data.get('user_id'),
                 created_at=datetime.utcnow()
                 order_details=json.dumps(data['order_details']))

    new_order.save()


def get_user_orders(event, context):
    results = big3d_table.scan(big3D_table.user_id == event["path"]["user_id"])

    return {"statusCode": 200, "body": json.dumps({"items": [dict(result) for result in results]})}
