FROM python:3.10.6

RUN mkdir -p /usr/src/unitbot
WORKDIR /usr/src/unitbot

COPY . .

RUN apt-get update -y && apt-get install python3-pip -y
RUN pip3 install pipenv && pipenv install

RUN chmod 0755 runbot.sh

ENTRYPOINT ["bash","/usr/src/unitbot/runbot.sh"]

