# Twitter Filtered Stream to Kafka Handler Package
Package: <a href="https://pypi.org/project/TwitterHandler">TwitterHandler-pypi</a>
## Description
It is a package that provides a simple way to filter Twitter Stream ingested to a Kafka topic.

**Data**:
- Twitter API v2 filtered stream endpoint

**Libraries:**
- Tweepy
- Kafka-python

## How to use it?
Use its API: <a href="https://github.com/HassanRady/Twitter-Handler-Api.git">Twitter-Handler-API github</a>

## Environment Variables
- `BEARER_TOKEN`: Twitter's API v2 bearer token.
- `KAFKA_HOST`: The Kafka broker host.
- `KAFKA_PORT`: The Kafka broker port.
- `KAFKA_TOPIC`: The Kafka broker topic.
