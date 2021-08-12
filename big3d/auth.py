import os

from pycognito import Cognito

from model import big3D_model
from big3d.utils import vaildate_incoming_data, validate_email

USER_POOL_ID = os.environ("USER_POOL_ID")


def create_new_user(event, context):
    data = json.loads(event["body"])

    if (
        found := validate_incoming_data(
            incoming=data,
            args=[
                "given_name",
                "family_name",
                "username",
                "email",
                "password",
            ],
        )
    ) is not None:
        return {"error_message": 422, "body": f"User has invalid field {found}"}

    if not validate_email(data["email"]):
        return {"error_message": 422, "body": "Invalid email format"}

    u = Cognito(USER_POOL_ID)

    u.set_base_attributes(
        email=data["email"],
        username=data["username"],
        family_name=data["family_name"],
        given_name=data["given_name"],
    )

    u.set_custom_attributes(id=str(uuid.uuid1()))

    u.register(data["username"], data["password"])

    u.confirm_sign_up("user_conf_code", username=data["username"])


# event.headers['id_token']


def authenticate_user(event, context):
    u = Cognito(USER_POOL_ID, email=event.get("email"))

    u.authenticate(password=event.get("password"))


def forgot_password(event, context):
    u = Cognito(USER_POOL_ID, email=event.get("email"))

    u.initiate_forgot_password()


def update_user(event, context):
    u = Cognito(USER_POOL_ID, event["body"].get("email"))

    u.update_profile(event["body"], attr_map=dict())


def check_auth(event, context):
    u = Cognito(USER_POOL_ID, id_token=event.headers["id_token"])
