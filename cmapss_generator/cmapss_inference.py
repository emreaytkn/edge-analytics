

import pandas as pd
import avro.schema
import io
from avro.io import DatumWriter, BinaryEncoder
from kafka import KafkaProducer

INPUT_TOPIC = 'cmapss-in'
OUTPUT_TOPIC = 'cmapss-output'
BOOTSTRAP_SERVERS= '127.0.0.1:9092'
ITEMS_TO_PREDICT = 10

class AvroInference():
    """Class representing a sink of Avro inference data to Apache Kafka.

        Args:
            boostrap_servers (str): List of Kafka brokers
            topic (str): Kafka topic 
            data_scheme_filename (str): Filename of the AVRO scheme for training data
            group_id (str): Group ID of the Kafka consumer. Defaults to sink

    """

    def __init__(self, boostrap_servers, topic,
        data_scheme_filename, group_id='sink'):
        
        self.boostrap_servers= boostrap_servers
        self.topic = topic

        self.data_scheme_filename = data_scheme_filename

        self.data_schema = open(self.data_scheme_filename, "r").read()

        self.avro_data_schema = avro.schema.Parse(self.data_schema)
        self.data_writer = DatumWriter(self.avro_data_schema)
      
        self.data_io = io.BytesIO()
        self.data_encoder = BinaryEncoder(self.data_io)
        self.__producer = KafkaProducer(
            bootstrap_servers=self.boostrap_servers
        )
    
    def send(self, data):
        
        self.data_writer.write(data, self.data_encoder)
        data_bytes = self.data_io.getvalue()

        self.__producer.send(self.topic, data_bytes)
        
        self.data_io.seek(0)
        self.data_io.truncate(0)
        """Cleans data buffer"""

    def close(self):
        self.__producer.flush()
        self.__producer.close()



# Read cmapss test dataset into pandas dataframe
cmapss_data = pd.read_csv("cmapss_test.csv")

features = pd.DataFrame(cmapss_data[cmapss_data.columns != "RUL"])

# Target column
remaining_useful_life = cmapss_data['RUL']

cmapss = AvroInference(boostrap_servers="localhost:9092", topic=INPUT_TOPIC, data_scheme_filename='data_schema.avsc')

