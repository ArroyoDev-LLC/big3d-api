import re


def validate_incoming_data(*, incoming, args):
    for arg in args:
        if not arg in incoming:
            return False
        if not incoming[arg]:
            return False
    return True


def validate_email(*, email_str):
    pattern = r"^[a-z]+[-_$.a-z]*@[a-z]*\.[a-z]+$"
    match = re.match(pattern, email_str, re.IGNORECASE)
    if match:
        return True
    else:
        return False
