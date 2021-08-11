def validate_incoming_data(*, incoming, model_args):
    for arg in model_args:
        if not arg in incoming:
            return False
        if not incoming[arg]:
            return False
    return True
