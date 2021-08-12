import json
from pathlib import Path

from awslambdaric.lambda_context import LambdaContext
from loguru import logger
from threedframe.config import config

# Setup threedframe.
DATA_DIR = Path("/tmp/big3d_api")
config.RENDERS_DIR = DATA_DIR / "renders"
config.setup_solid()


def hello(event, context: LambdaContext):
    logger.info("event: {} {}", event, dir(event))
    logger.info("context: {} {}", context, dir(context))
    logger.info(config.dict())
    body = {
        "message": "Go Serverless v2.0! Your function executed successfully!",
        "input": event,
        "time_remaining": context.get_remaining_time_in_millis(),
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
