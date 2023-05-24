FROM --platform=linux/amd64 python:3.12.0a7-bullseye AS builder
ENV PIPENV_IGNORE_VIRTUALENVS=1
WORKDIR /app
RUN pip install -U pip && pip install poetry \
    && poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install

FROM --platform=linux/amd64 python:3.12.0a7-slim-bullseye AS runtime
WORKDIR /app
RUN apt-get update && apt-get install -y libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
