![CI](https://github.com/nicolalamacchia/kwebmon/workflows/CI/badge.svg)

# kwebmon - a website health monitor

kwebmon is a website health monitor which periodically collects simple, very
basic, metrics from the specified websites.

`kwebmon` is a monorepo consisting of two separate Python packages.

`kwebmon_producer` monitors the websites and collects metrics. The collected
metrics are then sent to to a Kafka topic. `kwebmon_consumer` listens for
Kafka messages on the same topic and stores the received metrics in a
PostgreSQL database.

To check the status of a website, kwebmon sends a `GET` request and analyzes
the reponse.

The following metrics will be collected:

* response time (relative to the network kwebmon is deployed to);
* HTTP response status code;
* optionally, wheather the response body contains a specified RegEx pattern.

## Configuration

To be able to work, kwebmon needs some basic configuration:

* PostgreSQL connection URI;
* Kafka connection URI;
* access files required to connect to Kafka:
  - SSL key file;
  - SSL certificate file;
  - CA certificate;
* a JSON file containing the list of websites to be monitored with their
  respective RegEx patterns (optional) used to validate the response content.

Refer to the documentation of [kwebmon_producer](producer/README.md) and
[kwebmon_consumer](consumer/README.md) for more details.

## Usage

`kwebmon` uses `make` recursively to manage `kwebmon_producer` and
`kwebmon_consumer`. Run:

```sh
$ make help
```

for a list of available `make` targets.

## Caveats

kwebmon uses `psycopg2-binary` to connect to the PostgreSQL database.
[Psycopg's documentation](https://www.psycopg.org/docs/install.html#psycopg-vs-psycopg-binary)
advices against the use of such package in production in favor of `psycopg2`,
compiled from source.

Keep this in mind if you plan to deploy kwebmon in a production environment.

There might be a migration to `psycopg2` in the future.

## Useful Reading

To easily learn how to work with Kafka and Python (using
`kafka-python`):
https://aiven.io/blog/create-your-own-data-stream-for-kafka-with-python-and-faker
