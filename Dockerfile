FROM node:20-alpine as fe-build-stage
COPY ./src/js/chef .
RUN npm run build


FROM python:3.11.1 as be-build-stage
COPY pyproject.toml .
COPY poetry.lock .
RUN pip install poetry
COPY src/python ./src/python
COPY ./README.md .
RUN poetry build


FROM python:3.11.1-alpine

WORKDIR app

ENV PERSISTENT_ROOT="/chef/data"

ENV SERVE_FRONTEND="true"
ENV SERVE_FRONTEND_PATH="./static"
ENV LOG_FILE="$PERSISTENT_ROOT/chef.log"
ENV IMAGES_FOLDER="$PERSISTENT_ROOT/images"
ENV DATABASE_URI="sqlite:///$PERSISTENT_ROOT/chef.db"
ENV LOG_SQL="false"

RUN mkdir -p $IMAGES_FOLDER

COPY --from=be-build-stage dist/*.whl wheels/
RUN pip install wheels/*

COPY --from=fe-build-stage dist ./static

CMD chef
