FROM python:3.7.3-alpine

ENV WORKDIR blueprint
RUN mkdir /$WORKDIR
WORKDIR /$WORKDIR
COPY . .

RUN apk add build-base
RUN pip install pipenv && pipenv install

EXPOSE 8080

ENTRYPOINT pipenv run python3 /$WORKDIR/app.py
