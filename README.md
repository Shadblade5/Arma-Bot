# BR1-BOT

## Setup for Development

Create a new directory here named `.venv`, if you have hidden files/folders enabled, you should disable that so you can see it

Install pipenv and run `pipenv install --dev` to setup dependencies and virtual environment.

Install pre-commit by running `pre-commit install`, this will ensure pre-commit checks are run before commits

## Setup for Deployment

Create a new directory here named `.venv`, if you have hidden files/folders enabled, you should disable that so you can see it

Install pipenv and run `pipenv install` to setup dependencies and virtual environment.

Run the bot by executing `runbot.sh`

## Docker deployment

Install Docker and docker-compose on the host machine.

Deploy the bot by using `docker compose up -d` to deploy detached. To check status, use `docker compose ps` to view container statuses.
