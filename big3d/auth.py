import os
import json

from pycognito import Cognito

from big3d.model import big3D_table
from big3d.utils import validate_email

USER_POOL_ID = os.environ.get("USER_POOL_ID")
CLIENT_ID = os.environ.get("CLIENT_ID")


def validate_incoming_data(*, incoming, args):
    for arg in args:
        if not arg in incoming:
            return False
        if not incoming[arg]:
            return False
    return True


def create_new_user(event, context):
    data = json.loads(event["body"])

    if not validate_email(email_str=data["email"]):
        return {"error_message": 422, "body": "Invalid email format"}

    u = Cognito(USER_POOL_ID)

    u.set_base_attributes(
        email=data["email"],
        username=data["username"],
        family_name=data["family_name"],
        given_name=data["given_name"],
    )

    u.set_custom_attributes(id=str(uuid.uuid1()))

    print(data["username"], data["password"])
    u.register(data.get("username"), data.get("password"))

    u.confirm_sign_up("user_conf_code", username=data["username"])

    return json.dumps(u)


# event.headers['id_token']


def authenticate_user(event, context):
    u = Cognito(USER_POOL_ID, username=event.get("username"))

    u.authenticate(password=event.get("password"))


def forgot_password(event, context):
    u = Cognito(USER_POOL_ID, email=event.get("email"))

    u.initiate_forgot_password()


def update_user(event, context):
    u = Cognito(USER_POOL_ID, event["body"].get("email"))

    u.update_profile(event["body"], attr_map=dict())


def check_auth(event, context):
    u = Cognito(USER_POOL_ID, id_token=event.headers["id_token"])
