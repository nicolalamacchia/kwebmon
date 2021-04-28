# kwebmon Producer

Monitors websites and produces metrics for kwebmon Consumer.

The producer works by monitoring periodically the websites specified in the
configuration file and validating their content using regular expressions.

The metrics produced are:

* response time (relative to the network kwebmon is deployed to);
* HTTP response status code;
* optionally, wheather the response body contains a specified RegEx pattern.

## Websites Configuration

The main configuration file for kwebmon Producer is the list of websites to
be monitored. This configuration file needs to be in the following format:

```json
{
  "sites": [
    {
      "url": "https://example.net",
      "pattern": "Example D\\w+n"
    },
    {
      "url": "https://example.com"
    }
  ]
}
```

The `url` attribute must be a valid URL. It represents the URL to be checked,
which needs to allow `GET` requests. Duplicate URLs are not allowed.

The `pattern` attribute, if present, must be a Python-compatible RegEx
pattern (backslashes must be escaped). It is a pattern that will be searched
for in the body of the response (if any).

## Kafka Configuration

In order to connect the producer to the Kafka service, it is required to
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

By default the producer will look for the following file respectively in the
same directory it is launched from:

* `kafka-service.key`;
* `kafka-service.cert`;
* `kafka-ca.pem`.

To use different locations, specify them respectively in the following
environment variables:

* `KWEBMON_KAFKA_KEY`;
* `KWEBMON_KAFKA_CERT`;
* `KWEBMON_KAFKA_CA`.

## Run Locally

### Prerequisites

* GNU Make;
* Python 3.9;

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
$ pipenv run python -m kwebmon_producer -h
```

You can then run the producer with the desired argument:

```sh
$ pipenv run python -m kwebmon_producer <arguments>
```

### Launch the Producer

To execute the producer locally, run:

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
variables and change the check interval (5 seconds by default) and the Kafka
topic (which is `kwebmon` by default) by using CLI arguments.

For more details refer to
[Detailed Usage Information](#detailed-usage-information)
