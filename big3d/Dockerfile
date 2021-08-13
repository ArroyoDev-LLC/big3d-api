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
    && mkdir -p ${PACKAGES_DIR}

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

# Open3D + OpenSCAD + Blender deps
RUN curl -L -o /get-oscad-deps.sh https://raw.githubusercontent.com/openscad/openscad/openscad-2021.01/scripts/uni-get-dependencies.sh \
    && curl -L -o /check-oscad-deps.sh https://raw.githubusercontent.com/openscad/openscad/openscad-2021.01/scripts/check-dependencies.sh \
    && chmod +x /get-oscad-deps.sh && chmod +x /check-oscad-deps.sh \
    && apt-get update && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        git \
        cmake \
        libgmp-dev \
        libmpfr-dev \
        libgmpxx4ldbl \
        libboost-dev \
        libboost-thread-dev \
        zip unzip patchelf \
        # Open3D specific
        libgl1 \
        libgomp1 \
        libusb-1.0-0 \
        # Blender specific
        curl \
        libfreetype6 \
        libglu1-mesa \
        libxi6 \
        libxrender1 \
        xz-utils \
        # OpenSCAD specific
        libunistring-dev \
        libglib2.0 \
        libharfbuzz-dev \
     && /get-oscad-deps.sh \
     && /check-oscad-deps.sh \
     && apt-get clean \
     && rm -rf /var/lib/apt/lists/*

# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy OpenSCAD & Blender binaries
COPY --from=build-image /usr/local/bin/openscad /usr/local/bin/openscad
COPY --from=build-image /usr/local/blender /usr/local/blender/
RUN ln -s /usr/local/blender/blender /usr/local/bin/blender


# Copy fonts.
COPY --from=build-image /usr/share/fonts/truetype/opensans /usr/share/fonts/truetype/opensans

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
CMD [ "handler.handler" ]
