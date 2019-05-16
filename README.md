# Airtech Flight Booking System
An flight booking API for a fictional company Airtech to automate their current spreadsheet based system.

The API is built on Django and Django Rest Framework, Postgres database, Redis queues and caches. It is configured for deployment to AWS.

## Features
1. User registration and login
2. Booking and reserving flight tickets
3. Online purchase of tickets (stripe payment processing)
4. Flight status updates
5. Flight booking updates

## Requirements
- Pyenv (with Python 3.7.2)
- Pipenv
- Postgres 11+
- Redis 3+
- AWS Account

## Installation
First setup `pyenv` on your local machine. Instructions [here](https://github.com/pyenv/pyenv)

If you haven't added Python 3.7.2 to your `pyenv`, run the following command:
```
pyenv install 3.7.2
```
Navigate to the project root and set the local Python version to 3.7:
```
pyenv local 3.7.2
```
Install `pipenv`:
```
pip install pipenv
```
Install the project dependencies:
```
pipenv install
```
Run the project:
```
pipenv run start
```
