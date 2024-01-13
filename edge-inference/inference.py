
import json
import pickle
import uuid
from decoder import *

from confluent_kafka import Producer, Consumer

INPUT_TOPIC = 'cmapss-in'
OUTPUT_TOPIC = 'cmapss-output'
MAX_MESSAGES_TO_COMMIT = 20

def get_model():
    model = pickle.load(open("../model/baseline_rf_reg_v2.pkl", 'rb'))
    return model

if __name__ == '__main__':

    model = get_model()

    experiment_id = str(uuid.uuid4())

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

    output_producer = Producer({ 'bootstrap.servers': 'localhost:9092' })
    print(f"Kafka producer instantiated on the topic: {OUTPUT_TOPIC}")
    
    commitedMessages = 0
    
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
            prediction = model.predict([input])

            print(f"PRED: {prediction}")

            response = {
                'prediction': prediction[0],
                'experimentId': experiment_id
            }
            push_to_kafka = json.dumps(response).encode()
            output_producer.produce(OUTPUT_TOPIC, push_to_kafka, headers=msg.headers())
            output_producer.flush()

            print(f"--- Inference: END ---")

            commitedMessages += 1

            if commitedMessages >= MAX_MESSAGES_TO_COMMIT:          
                consumer.commit()
                commitedMessages = 0

                print(f"--- Inference: COMMIT ---")

        except Exception as e:
            print(f"Error while receiving data:  {str(e)}")




