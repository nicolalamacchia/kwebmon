FROM python:3-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

WORKDIR /opt/kwebmon/consumer

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pip install pipenv
RUN pipenv install --deploy --system

COPY . .

ENTRYPOINT ["python", "-m", "kwebmon_consumer"]
