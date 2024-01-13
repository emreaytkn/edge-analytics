
from socket import timeout
import numpy as np
import json
import pickle

from confluent_kafka import Producer, Consumer

def get_model():
    model = pickle.load(open("../baseline_rf_reg.pkl", 'rb'))
    return model

if __name__ == '__main__':
    model = get_model()

    input_topic = "mqtt.random.cmaps"

    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'test-group-id',
        'auto.offset.reset': 'earliest',            # Consumer starts from the earliest message in the topic
        'enable.auto.commit': False                 # Prevent consumer from auto commit the offset after processing a msg
    })
    consumer.subscribe([input_topic])

    print(f"Kafka consumer listening the topic: {input_topic}")

    while True:
        msg = consumer.poll(1.0)

        if msg:
            print(json.loads(msg.value()))
            #for topic, partition, offset, key, value in msg.items():
            #    print("Topic: {} | Partition: {} | Offset: {} | Key: {} | Value: {}".format(
            #        topic, partition, offset, key, value.decode("utf-8")
            #    ))
        else:
            print("No new messages")




