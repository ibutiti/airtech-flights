# Airtech Flight Booking System
An flight booking API for a fictional company Airtech to automate their current spreadsheet based system.

The API is built on Django and Django Rest Framework, Postgres database, Redis queues and caches. It is configured for deployment to AWS.

[![CircleCI](https://circleci.com/gh/ibutiti/airtech-flights/tree/master.svg?style=svg)](https://circleci.com/gh/ibutiti/airtech-flights/tree/master)
[![Test Coverage](https://api.codeclimate.com/v1/badges/6bad4714d5087bcd1858/test_coverage)](https://codeclimate.com/github/ibutiti/airtech-flights/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/6bad4714d5087bcd1858/maintainability)](https://codeclimate.com/github/ibutiti/airtech-flights/maintainability)

[API Documentation](https://documenter.getpostman.com/view/3400181/S1Zw9B8Q)

## Features
1. User registration and login
2. Booking and reserving flight tickets
3. Online purchase of tickets (stripe payment processing)
4. Flight status updates
5. Flight booking updates

## Requirements
- Docker
- Docker Compose
- AWS Account

## Installation
First setup [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/) on your machine.

Start the Docker daemon.

Run the command `make start_logs` and the server should start up with the default settings.

The application will be accessible from `0.0.0.0:8000` on your browser or API Client (Such as [Postman](https://www.getpostman.com/)).

You can configure your own environment variables by making a copy of the `.env-sample` file and modifying the values on it. The file as is is appropriately setup for the development environment, just rename it to `.env`.

## Useful Commands
- `make start`

  Starts the project in the background
- `make start_logs`

  Starts the project in the foreground with docker output on the terminal

- `make start_build`

  Rebuilds the Docker images and starts the project as in `make start_logs`

- `make stop`

  Stops the Docker containers and cleans up

- `make bash`

  Starts a terminal inside the Docker environment

- `make clean`

  Stops the Docker containers, cleans up the containers and deletes any `.pyc` files

- `make shell_plus`

  Starts the project and creates an interactive Django shell

- `make psql`

  Starts the project and opens `psql` for postgres

## Documentation
The app documentation is accessible at `/docs/`.
