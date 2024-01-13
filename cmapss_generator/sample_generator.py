import threading
import json

import random
from time import sleep
from faker import Faker

# from kafka_producer import kafka_producer
from mqtt_producer import mqtt_publisher

GENERATOR_COUNT = 5
generator_id_counter = 1

fake = Faker()

class cmapss_random_generator():
  def __init__ (self) -> None:
    global generator_id_counter, fake
      
    print(f"Starting random generator {generator_id_counter}")
    self.coord = fake.local_latlng(country_code='TR', coords_only=False)
    self.engine_id = "engine" + str(generator_id_counter)
    generator_id_counter+=1
    self.temperature = 0
    self.pressure = 0
    self.fan_speed = 0
    
    self.base_fuel = random.randint(900, 1000)
    self.current_fuel = None

  def returnEngineID(self):
    return self.engine_id
  
  # HPC outlet temperature) (◦R)
  def returnTemperature(self):
    self.temperature = random.uniform(1571.04, 1616.91)
    return self.temperature

  # HPC outlet Static pressure) (psia)
  def returnPressure(self):
    self.pressure = random.uniform(46.85, 48.5300)
    return self.pressure
    
  # Physical Fan Speed (rpm)
  def returnFanSpeed(self):
    self.fan_speed = random.uniform(2388.05, 2388.56)
    return self.fan_speed
      
  def returnFuelLevel(self):
    fuel_used = random.randint(1, 10)
    if self.current_fuel == None:
        self.current_fuel = self.base_fuel - fuel_used
    else:
      if self.current_fuel <= 0:
        refill = random.randint(500, 1000)
        self.current_fuel = self.current_fuel + refill
      else:
        self.current_fuel = self.current_fuel - fuel_used
        
    return self.current_fuel



def runCmapssRandomGenerator():
  cmapssGenerator = cmapss_random_generator()

  # kafkaProducer = kafka_producer()
  mqttProducer = mqtt_publisher(address="localhost", port=1883, clientID = cmapssGenerator.returnEngineID())
  mqttProducer.connect_client()

  sleeptime = random.randint(5, 10)
  
  while (True):
    cmapss_random_payload = {
      "engine_id": cmapssGenerator.returnEngineID(), 
      "lat": float (cmapssGenerator.coord[0]), 
      "lon": float(cmapssGenerator.coord[1]),
      "hpc_outlet_temp": cmapssGenerator.returnTemperature(), 
      "hpc_outlet_pressure": cmapssGenerator.returnPressure(), 
      "fan_speed": cmapssGenerator.returnFanSpeed(),
      "fuel": cmapssGenerator.returnFuelLevel() 
    }
    
    print(cmapss_random_payload, flush=True)
    
    # To listen messages: mosquitto_sub -v -t cmapss_random_generator
    mqttProducer.publish_to_topic(topic="cmapss-random-generator", data=cmapss_random_payload)
    
    sleep(sleeptime)

 
if __name__ == "__main__":
  
  x = 1
  while (x <= GENERATOR_COUNT):
    generator = threading.Thread(target=runCmapssRandomGenerator, daemon=True)
    generator.start()
    x+=1
    sleep(1)
  sleep(2000)