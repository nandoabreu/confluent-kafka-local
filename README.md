# confluent-kafka-local

A simple localhost running Apache Kafka implementation using confluent-kafka.

This implementation is based on [Confluent's Quick Start using Docker](https://docs.confluent.io/platform/current/quickstart/ce-docker-quickstart.html), 
but I needed a lighter version for my development/study and with access from my host (I didn't want 
an extra container) without messing my machine. [This article by Robin
Moffatt](https://www.confluent.io/blog/kafka-client-cannot-connect-to-broker-on-aws-on-docker-etc/) 
helped to understand communication between Zookeeper (configurations) and Kafka Broker.

## Requirements
- Docker  
- Python 3.8+  
- Python Poetry (required for tests)  
- My [http-web-server-json](https://github.com/nandoabreu/http-web-server-json) (optional)

## Initiate

```
make run-kafka

make install
make test-produce
make test-consume
```

## Expected responses
```
make test-produce
info: server:port is localhost:9092
debug: Message delivered to test_topic, partition 0: {"key": "244a5d38de0635526dbf9f658ccbc698", "method": "manual"}
debug: Message delivered to test_topic, partition 0: {"response_at": "2021-03-21 15:45:20.590626", "response_by": "b625ce879323", "method": "GET"}
```
```
make test-consume
debug: Try to retrieve up to 5 messages from test_topic @ localhost:9092
info: Message retrieved from test_topic: {"key": "244a5d38de0635526dbf9f658ccbc698", "method": "manual"}
```

## Stop
```
make stop
```

## TODO
- Add logging
- Move stdout prints to logging

## License
[MIT](LICENSE)
