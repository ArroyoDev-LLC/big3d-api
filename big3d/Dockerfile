# Define custom function directory
ARG FUNCTION_DIR="/function"
ARG PACKAGES_DIR="/packages"

FROM ghcr.io/arroyodev-llc/threedframe:latest as build-image

# Include global arg in this stage of the build
ARG FUNCTION_DIR
ARG PACKAGES_DIR

# Install aws-lambda-cpp build dependencies
RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev \
  git

# Create function/packages dirs
RUN mkdir -p ${FUNCTION_DIR} \
    && mkdir -p ${PACKAGES_DIR} \

# Copy function requirements.
COPY requirements.txt .

# Install the function's dependencies
#: threedframe package lives @ /app
RUN pip install --no-cache-dir -U pip \
    && pip --no-cache-dir install \
        --target ${PACKAGES_DIR} \
          awslambdaric \
          /app \
          -r requirements.txt

# Copy rest of function code.
COPY ./* ${FUNCTION_DIR}


### Function handler stage.
FROM python:3.8-buster

# Include global arg in this stage of the build
ARG FUNCTION_DIR
ARG PACKAGES_DIR

# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
COPY --from=build-image ${PACKAGES_DIR} ${PACKAGES_DIR}

# Copy entrypoint.
COPY ./scripts/docker-entry-point.sh /docker-entrypoint.sh
COPY ./scripts/aws-lambda-rie /usr/local/bin/aws-lambda-rie

# Lambdas only have write access @ /tmp
ENV HOME "/tmp/big3d_api"
# Direct python path to packages dir.
ENV PYTHONPATH ${PACKAGES_DIR}

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD [ "handler.hello" ]
