run-kafka:
	docker run --network host --rm --detach --name zookeeper -e ZOOKEEPER_CLIENT_PORT=2181 confluentinc/cp-zookeeper:5.5.0
	docker run --network host --rm --detach --name broker \
		-e KAFKA_BROKER_ID=1 \
		-e KAFKA_ZOOKEEPER_CONNECT=localhost:2181 \
		-e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
		-e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
		confluentinc/cp-kafka:5.5.0

install:
	poetry install

test-produce:
	poetry run python kafka_test-produce.py

test-consume:
	poetry run python kafka_test-consume.py

stop:
	docker stop broker
	docker stop zookeeper
