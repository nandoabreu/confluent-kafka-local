from confluent_kafka.admin import AdminClient
from confluent_kafka import Producer
from sys import argv
from datetime import datetime
import hashlib
import requests
import json


def Produce(serverXport, topic, records):
    p = Producer({'bootstrap.servers': serverXport})

    def delivery_report(err, records):
        if err is not None:
            print('alert: Message delivery failed: {err}')
        else:
            print(f"debug: Message delivered to {records.topic()}, partition {records.partition()!r}: {records.value().decode('utf-8')}")

    for data in records:
        p.poll(0)
        p.produce(topic, data.encode('utf-8'), callback=delivery_report)

    r = p.flush(timeout=5)
    if r > 0:
        print(f'error: Message not produced ({r} message(s) lost, maybe timeout?)')

def request_json(request_json_url):
    res = []

    # GET
    try:
        r = requests.get(request_json_url)
        data = r.json()
        data['method'] = 'GET'
        res.append(json.dumps(data))
    except Exception as e:
        print(f'alert: Could not send GET to {request_json_url} ({str(e)[:100]})')

    # POST
    try:
        payload = {'key': hashlib.md5(str(datetime.now()).encode('utf-8')).hexdigest()}
        r = requests.post(request_json_url, data=json.dumps(payload), headers={'content-type': 'application/json'})
        data = r.json() # creates dict
        data['method'] = 'POST'
        res.append(json.dumps(data))
    except Exception as e:
        print(f'alert: Could not send POST to {request_json_url} ({str(e)[:100]})')

    return res


def main():
    topic = 'test_topic'
    request_json_url = 'http://0.0.0.0:5000/'

    try:
        serverXport = argv[1]
    except:
        serverXport = 'localhost:9092'
    finally:
        print(f'info: server:port is {serverXport}')

    try:
        broker = AdminClient({'bootstrap.servers': serverXport}) # Test connection
        md = broker.list_topics(timeout=10)
    except Exception as e:
        raise e

    try:
        md5 = hashlib.md5(str(datetime.now()).encode('utf-8')).hexdigest()
        Produce(serverXport, topic, [json.dumps({'key': md5, 'method': 'manual'})])

        res = request_json(request_json_url)
        if res:
            Produce(serverXport, topic, request_json(request_json_url))
    except Exception as e:
        raise e

if __name__ == '__main__':
    main()
