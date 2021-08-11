import json

from loguru import logger


def hello(event, context):
    logger.info("event: {} {}", event, dir(event))
    logger.info("context: {} {}", context, dir(context))
    body = {
        "message": "Go Serverless v2.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
