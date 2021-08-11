FROM ghcr.io/arroyodev-llc/threedframe:latest as build

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app/
COPY pyproject.toml poetry.lock* /app/

# Build wheel.
RUN bash -c "poetry export --without-hashes -o requirements.txt && pip install -U pip && mkdir -p dist && pip wheel -w dist -r requirements.txt"

WORKDIR /wheels
RUN bash -c "cp /app/dist/* /wheels/ && cp /app/requirements.txt /wheels/ && rm -rf /app"



FROM public.ecr.aws/lambda/python:3.8

# Copy OpenSCAD & Blender binaries
COPY --from=build /usr/local/bin/openscad /usr/local/bin/openscad
COPY --from=build /usr/local/blender /usr/local/blender

# Copy fonts
COPY --from=build /usr/share/fonts/truetype/ /usr/share/fonts/truetype/

# Install api deps.
COPY --from=build /wheels /wheels
RUN pip install --no-cache-dir -U pip \
  && pip install --no-cache-dir -f /wheels/ -r /wheels/requirements.txt \
  && rm -rf /wheels

COPY . .

CMD ["handler.hello"]
