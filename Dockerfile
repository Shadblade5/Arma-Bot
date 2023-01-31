FROM python:3.10.6-slim

RUN mkdir -p /usr/src/unitbot
WORKDIR /usr/src/unitbot

COPY . .

RUN chmod 0755 runbot.sh

ENTRYPOINT ["sh","/usr/src/unitbot/runbot.sh"]
