


After configuring the mqtt proxy, then it should start ingesting data from MQTT broker directly.

> kafka-console-consumer --bootstrap-server localhost:9092 --topic mqtt.random.cmaps --from-beginning


Phyton CMAPSS Inference App : edge-inference/inference.py
> python inference.py

- Listens to CMAPSS_INPUT_TOPIC (**cmapss_in**)
- Gets the streaming data in *AVRO* format, decodes it and prepares for inference
- Use pretrained model to infer RUL - push to CMAPSS_OUTPUT_TOPIC (**cmapss_output**)


kafka-console-consumer --bootstrap-server localhost:9092 --topic cmapss-out  --from-beginning

Test data - kafka consumer cmapss-in


Clear all the historical data in a Kafka topic:
