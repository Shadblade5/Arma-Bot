FROM python:3.10.6

RUN mkdir -p /usr/src/unitbot
WORKDIR /usr/src/unitbot

COPY . .

RUN "apt-get update && apt-get install python3-pip"

RUN "pip3 install pipenv && pipenv install"

ENTRYPOINT [ "runbot.sh" ]
