FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add --no-cache mariadb-dev

WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apk del build-deps
EXPOSE 8000
