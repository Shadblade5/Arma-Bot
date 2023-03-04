FROM python:3.10.6-slim

RUN mkdir -p /usr/src/unitbot
WORKDIR /usr/src/unitbot

RUN apt-get update -y \
    && apt-get install python3-pip -y --no-install-recommends \
    && apt-get install git -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --no-cache-dir pipenv

COPY Pipfile* ./

RUN pipenv install --keep-outdated

COPY . .

RUN chmod 0755 runbot.sh

ENTRYPOINT ["sh","/usr/src/unitbot/runbot.sh"]
