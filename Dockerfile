FROM python:3.10.6-slim

RUN mkdir -p /usr/src/unitbot
WORKDIR /usr/src/unitbot

COPY . .

RUN apt-get update -y && apt-get install python3-pip -y && pip3 install --no-cache-dir pipenv

RUN chmod 0755 runbot.sh

ENTRYPOINT ["sh","/usr/src/unitbot/runbot.sh"]
