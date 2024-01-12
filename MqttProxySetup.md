
- [Setup Confluent](#setup-kafka-clusters)

- [Setup Kafka Clusters](#setup-kafka-clusters)

- [Setup Mqtt Broker](#setup-mqtt-broker)


# Setup Confluent Platform

Confluent Inc., a company founded by the creators of Apache Kafka, provides the **Confluent Platform** which is built around Apache Kafka and extend its capabilities. The platform offers additional tools and services for managing, monitoring, and deploying Kafka-based solutions. Platform also offers *Confluent Cloud*, a fully managed cloud service for Apache Kafka.

> [!TIP]
> Confluent local setup needs either Java 8 or 11. Consider managing different versions of Java with brew or SDKMAN.

> export JAVA_HOME=`/usr/libexec/java_home -v 11` 

The open-source and community features of Confluent Platform can be downloaded from [Community](https://www.confluent.io/installation/) section. In order to locally test the infrastructure, the ZIP version of Confluent Platform v7.5.2 is downloaded and unzipped to a desired location.

Confluent CLI should be installed seperately:

> export CONFLUENT_HOME=\<The directory where Confluent is installed>

> brew install confluentinc/tap/cli

> confluent local services start

```
Starting Zookeeper
Zookeeper is [UP]
Starting Kafka
Kafka is [UP]
Starting Schema Registry
Schema Registry is [UP]
Starting Kafka REST
Kafka REST is [UP]
Starting Connect
Connect is [UP]
Starting KSQL Server
KSQL Server is [UP]
Starting Control Center
Control Center is [UP]
```

This manual assumes that the services Zookeeper, Kafka, Connect, and MQTT Broker use default values.

In order to check the status of core services:

> confluent local services status

## Setup Kafka Clusters

For seting up the MQTT-proxy, we need to install a **Kafka Connect** plugin named [kafka-connect-mqtt v1.7.1](https://www.confluent.io/hub/confluentinc/kafka-connect-mqtt) for sending and receiving data from a Mqtt broker. Download ZIP version, and extract it onto one of the directories that is listed on the Connect worker's *plugin.path* configuration properties.



## Setup Mqtt Broker

Start the MQTT Broker and test publish / subscribe with 'dummy' topic:

```
brew services start mosquitto
mosquitto_sub -h 127.0.0.1 -t dummy
mosquitto_pub -h 127.0.0.1 -t dummy -m "Hello world"
```

Please note that Confluent CLI changed with Confluent Platform 5.3+: 'confluent local start' Confluent Platform 5.2 and earlier: 'confluent start'. This guide is tested with Confluent Platform 5.4.0.

We use Kafka Connect in distributed mode via REST call (only possible when Connect is running). This is highly recommend as you can do this for one single node (like in this example, but also deploy a distributed Connect cluster).

Important: If you copy&paste the below curl command, make sure that you copy it "plaintext only". Otherwise, it might not work. On my Mac, I copy the command to a text editor first and from there to the command line to execute it.

```
curl -s -X POST -H 'Content-Type: application/json' http://localhost:8083/connectors -d '{
    "name" : "mqtt-source",
"config" : {
    "connector.class" : "io.confluent.connect.mqtt.MqttSourceConnector",
    "tasks.max" : "1",
    "mqtt.server.uri" : "tcp://127.0.0.1:1883",
    "mqtt.topics" : "temperature",
    "kafka.topic" : "mqtt.temperature",
    "confluent.topic.bootstrap.servers": "localhost:9092",
    "confluent.topic.replication.factor": "1",
    "confluent.license":""
    }
}'
```