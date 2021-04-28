FROM python:3-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

WORKDIR /opt/kwebmon/producer

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pip install pipenv
RUN pipenv install --deploy --system

COPY . .

ENTRYPOINT ["python", "-m", "kwebmon_producer"]
