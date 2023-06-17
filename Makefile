PHONY: build up stop down startapp makemigrations migrate shell test update_lock black isort flake8 pytest mypy showmigrations check_all

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
	docker compose run --rm api python manage.py makemigrations --name ${name}

showmigrations:
	docker compose run --rm api python manage.py showmigrations

migrate:
	docker compose run --rm api python manage.py migrate ${app_name} ${migration_name}

shell:
	docker compose run --rm api python manage.py shell

test:
	docker compose run --rm api pytest -v ${file}

update_lock:
	docker compose run --rm api poetry lock

black:
	docker compose run --rm api black .

isort:
	docker compose run --rm api isort .

flake8:
	docker compose run --rm api flake8

mypy:
	docker compose run --rm api mypy .

check_all:
	docker compose run --rm api black . && \
	docker compose run --rm api isort . && \
	docker compose run --rm api flake8 && \
	docker compose run --rm api mypy . && \
	docker compose run --rm api pytest