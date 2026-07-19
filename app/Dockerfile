FROM python:3.12.7-slim

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

COPY . .