package com.edge.analytics.configuration;

import org.apache.kafka.clients.admin.AdminClientConfig;
import org.apache.kafka.clients.admin.NewTopic;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.config.TopicBuilder;
import org.springframework.kafka.core.KafkaAdmin;

import java.util.HashMap;
import java.util.Map;

@Configuration
public class KafkaTopicConfig {

    @Value(value = "${spring.kafka.bootstrap-servers}")
    private String bootstrapAddress;

    @Value(value = "${message.topic.name}")
    private String topicName;

    // KafkaAdmin Spring bean automatically add topics for all beans of type NewTopic

    public KafkaAdmin kafkaAdmin() {
        Map<String, Object> configs = new HashMap<>();
        configs.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapAddress);
        return new KafkaAdmin(configs);
    }

    @Bean
    public NewTopic topic1() {
        return new NewTopic(topicName, 1, (short)1);
    }

    @Bean
    public NewTopic mqttProxyTopic() {
        return new NewTopic("mqtt.random.cmaps", 1, (short)1);
    }

    @Bean
    public NewTopic cmapssPredictionTopic() {
        return new NewTopic("cmapss-output", 1, (short)1);
    }

}
