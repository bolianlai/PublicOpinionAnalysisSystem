from confluent_kafka import Consumer, KafkaError


c = Consumer({
    'bootstrap.servers': '127.0.0.1:9092',
    'group.id': 'test',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['test-1'])
i = 0
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