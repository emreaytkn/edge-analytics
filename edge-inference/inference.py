
from socket import timeout
import json
import pickle

from decoder import *

from confluent_kafka import Producer, Consumer

INPUT_TOPIC = 'cmapss-in'
OUTPUT_TOPIC = 'cmapss-out'

def get_model():
    model = pickle.load(open("../model/baseline_rf_reg_v2.pkl", 'rb'))
    return model

if __name__ == '__main__':

    model = get_model()

    input_format = "AVRO"
    data_schema = "../schema/data_schema.avsc"

    # input_topic = "mqtt.random.cmaps"

    decoder = DecoderFactory.get_decoder(input_format, data_schema=data_schema)

    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'test-group-id',
        'auto.offset.reset': 'earliest',            # Consumer starts from the earliest message in the topic
        'enable.auto.commit': False                 # Prevent consumer from auto commit the offset after processing a msg
    })
    consumer.subscribe([INPUT_TOPIC])

    print(f"Kafka consumer listening the topic: {INPUT_TOPIC}")

    while True:
        msg = consumer.poll(1.0)
        
        if msg is None:
            continue
        
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        try:
            
            print(f"--- Inference: START ---")

            input = decoder.decode(msg.value())
            prediction_output = model.predict([input])

            print(f"PRED: {prediction_output}")


        except Exception as e:
            print(f"Error while receiving data:  {str(e)}")




