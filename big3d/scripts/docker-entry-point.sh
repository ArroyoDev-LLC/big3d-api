#!/bin/sh

if [ -z "${AWS_LAMBDA_RUNTIME_API}" ]; then
  if [ -z "${IS_LOCAL}" ]; then
    exec /usr/local/bin/aws-lambda-rie /usr/local/bin/python -m awslambdaric $@
  else
    exec /packages/bin/uvicorn --host 0.0.0.0 --port 8080 --reload --reload-dir /function/ handler:app
  fi
else
  exec /usr/local/bin/python -m awslambdaric $@
fi
