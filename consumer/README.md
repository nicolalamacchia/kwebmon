# kwebmon Consumer

Consumes data coming from a kwebmon Producer and stores them to a PostgreSQL
database.

The default destination table name on the PostgreSQL database is
`kwebmon_metrics`. To change it, see [Advanced
Configuration](#advanced-configuration)

## Kafka Configuration

In order to connect the consumer to the Kafka service, it is required to
provide a connection URI to the service/cluster and access key files.

In a production environment the connection URI should be passed by defining
the `KWEBMON_KAFKA_URI` environmen variable. The connection URI is in the
form `hostname:port`.

The access file needed are:

* SSL key;
* SSL certificate;
* CA certificate.

Your Kafka service provider should allow you to download them. If you are
hosting the broker yourself, you will have to generate them.

By default the consumer will look for the following file respectively in the
same directory it is launched from:

* `kafka-service.key`;
* `kafka-service.cert`;
* `kafka-ca.pem`.

To use different locations, specify them respectively in the following
environment variables:

* `KWEBMON_KAFKA_KEY`;
* `KWEBMON_KAFKA_CERT`;
* `KWEBMON_KAFKA_CA`.

## PostgreSQL Configuration

In order to connect the consumer to the PostgreSQL database, it is required
to provide a connection URI to the database. See _§ Connection Strings_
[here](https://www.postgresql.org/docs/current/libpq-connect.html) for more
details.

In a production environment the connection URI should be passed by defining
the `KWEBMON_POSTGRES_URI` environmen variable.

The target database must be properly configured to allow writes on the
specified target table.

## Run Locally

### Prerequisites

* GNU Make;
* Python 3.9;
* a C compiler;
* `libpq-dev` (or another similar library providing the `libpq` header files
  and the `pg_config` executable);
* Python header files.

Refert to [Psycopg's documentation](https://www.psycopg.org/docs/install.html#build-prerequisites)
for more information about the last three points.

### Prepare the Environment

```sh
$ make init
```

### Usage Information

```sh
$ make help
```

### Detailed Usage Information

To show a list of available CLI arguments and defaults, run:

```sh
$ pipenv run python -m kwebmon_consumer -h
```

You can then run the consumer with the desired argument:

```sh
$ pipenv run python -m kwebmon_consumer <arguments>
```

### Launch the Consumer

To execute the consumer locally, run:

```sh
$ make run
```

or execute it through `pipenv` as shown above.

## Run Tests

```sh
$ make tests
```

## Advanced Configuration

It is possible to override the configuration provided by environment
variables and to change the database table name (`kwebmon_metrics` by
default) and the Kafka topic (`kwebmon` by default) by using CLI arguments.

For more details refer to
[Detailed Usage Information](#detailed-usage-information)
