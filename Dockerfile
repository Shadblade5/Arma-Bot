FROM python:3.10.6

RUN mkdir -p /usr/src/unitbot
WORKDIR /usr/src/unitbot

COPY . .

RUN "pip install pipenv && pipenv install"

ENTRYPOINT [ "runbot.sh" ]
