from confluent_kafka.admin import AdminClient
from confluent_kafka import Consumer
from sys import argv
import platform


def Consume(serverXport, topic):
    c = Consumer({
        'bootstrap.servers': serverXport,
        'group.id': 'python',
        'group.instance.id': platform.node(),
        'client.id': platform.node(),
        'auto.offset.reset': 'earliest',
    })

    c.subscribe([topic])

    try:
        print(f'debug: Try to retrieve up to 5 messages from {topic} @ {serverXport}')
        msgs = c.consume(num_messages=5, timeout=30)

        if len(msgs) < 1:
            print('alert: No message to consume (also check timeouts)')
        else:
            for msg in msgs:
                print(f"info: Message retrieved from {msg.topic()}: {msg.value().decode('utf-8')}")

    except Exception as e:
        raise e

    c.close()


def main():
    topic = 'test_topic'

    try:
        serverXport = argv[1]
    except:
        serverXport = 'localhost:9092'
    finally:
        print(f'info: serverXport is {serverXport}')

    try:
        broker = AdminClient({'bootstrap.servers': serverXport}) # Test connection
        md = broker.list_topics(timeout=10)
    except Exception as e:
        raise e

    try:
        Consume(serverXport, topic)
    except Exception as e:
        raise e


if __name__ == '__main__':
    main()
