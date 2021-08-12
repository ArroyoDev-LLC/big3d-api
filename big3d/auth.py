import os
import uuid
import json

import boto3

from pycognito import Cognito
from pycognito.aws_srp import AWSSRP

from big3d.model import Big3D
from big3d.utils import validate_email

USER_POOL_ID = os.environ.get("USER_POOL_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")


def create_new_user(event, context):

    data = json.loads(event["body"])

    if not validate_email(email_str=data.get("email")):
        return {"errorCode": 422, "body": "Invalid email format"}

    u = Cognito(
        USER_POOL_ID,
        CLIENT_ID,
        client_secret=CLIENT_SECRET,
    )

    u.set_base_attributes(
        email=data["email"],
    )

    u.add_custom_attributes(id=str(uuid.uuid1()))

    print(data["email"], data["password"])

    u.register(data["email"], data["password"], attr_map={"username": "email", "id": "id"})

    u.confirm_sign_up("user_conf_code", username=data["email"])

    return json.dumps(u)


def authenticate_user(event, context):
    u = Cognito(USER_POOL_ID, CLIENT_ID, username=event.get("email"))

    u.authenticate(password=event.get("password"))


def forgot_password(event, context):
    u = Cognito(USER_POOL_ID, CLIENT_ID, username=event.get("email"))

    u.initiate_forgot_password()


def confirm_forgot_password(event, context):
    u = Cognito(USER_POOL_ID, CLIENT_ID, username=body["username"])

    u.confirm_forgot_password(body["confirmation_code"], body["new_password"])


def update_user(event, context):
    u = Cognito(USER_POOL_ID, CLIENT_ID, event["body"].get("email"))

    u.update_profile(event["body"], attr_map=dict())


def check_auth(event, context):
    u = Cognito(
        USER_POOL_ID,
        CLIENT_ID,
        id_token=event.headers["id_token"],
        refresh_token=event.headers["refresh_token"],
        access_token=event.headers["access_token"],
    )

    u.check_token()


def get_user(event, context):
    u = Cognito(USER_POOL_ID, CLIENT_ID, username=event.body["email"])

    user = u.get_user(attr_map={"username": "email", "id": "id"})

    return json.dumps(user)
