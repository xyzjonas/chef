FROM node:20-alpine as fe-build-stage
COPY ./src/js/chef .
RUN npm run build


FROM python:3.11.1 as be-build-stage
COPY src/python ./src/python
COPY pyproject.toml .
COPY poetry.lock .
RUN pip install poetry
RUN poetry build


FROM python:3.11.1-buster

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# Install system dependencies
RUN set -e; \
    apt-get update -y && apt-get install -y \
    tini \
    libpq-dev \
    gcc \
    lsb-release; \
    gcsFuseRepo=gcsfuse-`lsb_release -c -s`; \
    echo "deb http://packages.cloud.google.com/apt $gcsFuseRepo main" | \
    tee /etc/apt/sources.list.d/gcsfuse.list; \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
    apt-key add -; \
    apt-get update; \
    apt-get install -y gcsfuse \
    && apt-get clean \
    && pip install psycopg2

WORKDIR /app

# GCP bucket will be mounted here using gcsfuse
ENV MNT_DIR="/chef/data"

ENV SERVE_FRONTEND="true"
ENV SERVE_FRONTEND_PATH="./static"
ENV LOG_FILE="$MNT_DIR/chef.log"
ENV IMAGES_FOLDER="$MNT_DIR/images"
ENV DATABASE_URI="sqlite:///$MNT_DIR/chef.db"
ENV LOG_SQL="false"

RUN mkdir -p $IMAGES_FOLDER

COPY --from=be-build-stage dist/*.whl wheels/
RUN pip install wheels/*

COPY --from=fe-build-stage dist ./static

COPY gcsfuse_run.sh .
RUN chmod +x /app/gcsfuse_run.sh

# Use tini to manage zombie processes and signal forwarding
# https://github.com/krallin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

CMD ["/app/gcsfuse_run.sh"]