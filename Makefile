PHONY: build up stop down startapp makemigrations migrate shell test update_lock black isort flake8 pytest mypy

build:
	docker compose build

up:
	docker compose up

stop:
	docker compose stop

down:
	docker compose down

startapp:
	docker compose run --rm api python manage.py startapp $(app_name)

makemigrations:
	docker compose run --rm api python manage.py makemigrations

migrate:
	docker compose run --rm api python manage.py migrate

shell:
	docker compose run --rm api python manage.py shell

test:
	docker compose run --rm api pytest

update_lock:
	docker compose run --rm api poetry lock

black:
	docker compose run --rm api black .

isort:
	docker compose run --rm api isort .

flake8:
	docker compose run --rm api flake8

pytest:
	doker compose run --rm api pytest ${file}

mypy:
	docker compose run --rm api mypy .