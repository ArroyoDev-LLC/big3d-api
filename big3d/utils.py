import re


def validate_incoming_data(*, incoming, args):
    for arg in model_args:
        if not arg in incoming:
            return False
        if not incoming[arg]:
            return False
    return True


def validate_email(*, email_str):
    pattern = r"^[a-z]+[-_$.a-z]*@[a-z]*\.[a-z]+$"
    match = re.match(pattern, "abc.xyz@gmail.com", re.IGNORECASE)

    return match
