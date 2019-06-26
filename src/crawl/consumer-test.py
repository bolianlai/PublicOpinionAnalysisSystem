
if __name__ == '__main__':
    from confluent_kafka import Consumer, KafkaError
    c = Consumer({
        'bootstrap.servers': '127.0.0.1:9091, 127.0.0.1:9092, 127.0.0.1:9093',
        'group.id': 'test',
        'auto.offset.reset': 'earliest'
    })
    c.subscribe(['test'])
    i = 0
    print('Start Consumer...')
    while True:
        i+=1
        msg = c.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        print('Received message: {}'.format(msg.value().decode('utf-8')))

    c.close()
    print('number: %s ' % i)