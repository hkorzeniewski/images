# images-api

## Summary


## Tech stack
* [Django (^4.0.6)](https://www.djangoproject.com/)
* [DRF (^3.13.1) API framework](https://www.django-rest-framework.org)
* [Poetry dependency manager ](https://pypi.org/project/poetry/)

Project is [dockerized](https://www.docker.com/).

## Local development setup

Prerequisites:

* [Python version 3.10.4+]()
* [poetry](https://python-poetry.org/docs/#installation)
* [pyenv - optional]() for virtualenv and python version management
* [docker](https://docs.docker.com/engine/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

There are two ways to work with this project on local environment:

### local virtualenv + DB in docker container (recomended)

1. Install `poetry` (check poetry setup below)
2. Install `docker` and `docker-compose`
3. Install `pyenv` (optional - check Pyenv setup below)
4. If you prefer pyenv create virtualenv `pyenv virtualenv 3.10.4 images-api` and activate it.
5. Install dependencies `poetry install`. This command will create the virtual env for you
6. Make migrations
    `python manage.py migrate`
7. Create superuser `python manage.py createsuperuser`
8. Create builtin AccountTiers model at first launch `python manage.py build_tiers_command`
9. Run django development server `python manage.py runserver 0.0.0.0:8000` or `make run-local`
10. Done

### Docker with docker-compose

1. Install `docker` and `docker-compose`
2. Run `docker-compose build`
3. Start all services `docker-compose up`. You can user `docker-compose up -d` for detached mode.
4. Log into app docker container `docker exec -it api_api_1 sh` (name of container may be different)
5. Make steps 7,8 from `local virtualenv + DB` instruction
6. Done

### Running tests locally:

    make flake
    make isort
    make bandit
    make linters
    make test

Commands are self explanatory - the minimal set is:

    make linters  # will do flake, isort and bandit
    make test  # will run django tests
