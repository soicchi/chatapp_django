FROM --platform=linux/amd64 python:3.12.0a7-bullseye AS builder
WORKDIR /app
RUN pip install -U pip && pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install

FROM --platform=linux/amd64 python:3.12.0a7-slim-bullseye
WORKDIR /app
RUN apt-get update && apt-get install -y libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
