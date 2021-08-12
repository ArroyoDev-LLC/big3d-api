import json
from pathlib import Path

from loguru import logger
from threedframe.config import config

# Setup threedframe.
DATA_DIR = Path("/tmp/big3d_api")
config.RENDERS_DIR = DATA_DIR / "renders"
config.setup_solid()


def hello(event, context):
    logger.info("event: {} {}", event, dir(event))
    logger.info("context: {} {}", context, dir(context))
    logger.info(config.dict())
    body = {
        "message": "Go Serverless v2.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
