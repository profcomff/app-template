# Сборка страниц с документацией
FROM node:18 AS build-docs
RUN npm i @diplodoc/cli -g

ADD ./docs /app/input-folder
RUN yfm -i /app/input-folder -o /app/ouput-folder


# Сборка UI
FROM node:18 AS build-ui
WORKDIR /app
ADD ./frontend/package.json ./frontend/package-lock.json /app/
RUN npm ci
ADD ./frontend /app
RUN npm run docker-build


# Сборка API с установкой зависимостей
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}
ENV APP_NAME=my_app_api
ENV APP_MODULE=${APP_NAME}.routes:app

COPY ./backend/requirements.txt /app/
RUN apt update && apt install -y nginx && pip install -U -r /app/requirements.txt

COPY ./backend/alembic.ini /alembic.ini
COPY ./backend/migrations /migrations/

COPY ./backend/${APP_NAME} /app/${APP_NAME}


# Копирование собранных UI и документации в директории сервера
ADD ./cicd/nginx.conf /etc/nginx/nginx.conf
COPY --from=build-docs /app/ouput-folder /app/docs
COPY --from=build-ui /app/dist /app/ui

RUN mkdir /usr/share/nginx/logs/ && touch /usr/share/nginx/logs/error.log

ENV GUNICORN_CMD_ARGS="-b 0.0.0.0:81 --log-level debug"
