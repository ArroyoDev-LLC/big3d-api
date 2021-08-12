import json
import uuid
from loguru import logging
from datetime import datetime

from email_validator import validate_email, EmailNotVaildError

from utils import validate_incoming_data
from functions.user_model import UserModel


def create_order(event, context):
    data = json.loads(event["body"])

    if not validate_incoming_data(
        incoming=data,
        model_args=[
            "id",
            "first_name",
            "last_name",
            "password",
            "email",
            "address",
            "billing_address",
        ],
    ):
        return {
            "statusCode": 422,
            "body": json.dumps({"error_message": "User does not contain all valid fields"}),
        }

    if not validate_email(data["email"]):
        return {"statusCode": 422, "body": json.dumps({"error_message": "Not a valid email form"})}

    new_user = UserModel(
        id=str(
            uuid.uuid1(),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            password=hash_pass(data.get("password")),
            address=data.get("address"),
            billing_address=data.get("billing_address"),
        )
    )

    new_user.save()

    return {"statusCode": 201, "body": json.dumps(dict(new_order))}
