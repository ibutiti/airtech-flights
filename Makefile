start: ## start api in bground
	@docker-compose up -d

start_logs:
	@docker-compose up

stop:
	@docker-compose stop

start_build:
	@docker-compose up --build

clean:
	@docker-compose down
	@find . -name \*.pyc -delete

bash: start
	@docker-compose exec web /bin/bash

shell_plus: start
	@docker-compose exec web python manage.py shell_plus

psql: start
	@docker-compose exec db psql -U postgres

migrations:
	@python manage.py makemigrations

migrate:
	@python manage.py migrate

test:
	@python manage.py test
	@rm -rf test-results
