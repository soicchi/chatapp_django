PHONY: build up stop down startapp makemigrations migrate shell test

build:
	docker compose build

up:
	docker compose up

stop:
	docker compose stop

down:
	docker compose down

startapp:
	docker compose run --rm web python manage.py startapp $(app_name)

makemigrations:
	docker compose run --rm web python manage.py makemigrations

migrate:
	docker compose run --rm web python manage.py migrate

shell:
	docker compose run --rm web python manage.py shell

test:
	docker compose run --rm web pytest
