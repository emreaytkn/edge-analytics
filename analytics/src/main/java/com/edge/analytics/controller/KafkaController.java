package com.edge.analytics.controller;

import com.edge.analytics.kafka.MessageProducer;
import lombok.AllArgsConstructor;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StoreQueryParameters;
import org.apache.kafka.streams.state.QueryableStoreTypes;
import org.apache.kafka.streams.state.ReadOnlyKeyValueStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.config.StreamsBuilderFactoryBean;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
@AllArgsConstructor
public class KafkaController {

    private final StreamsBuilderFactoryBean factoryBean;

    @Autowired
    private MessageProducer messageProducer;

    @PostMapping("/kafka/test")
    public String sendMessage(@RequestBody String message) {
        messageProducer.sendMessage(message);
        return "Message sent: " + message;
    }

    @PostMapping("/kafka/test/stream")
    public Long getWordCount(@RequestBody String word) {
        KafkaStreams kafkaStreams = factoryBean.getKafkaStreams();
        ReadOnlyKeyValueStore<String, Long> counts = kafkaStreams.store(
                StoreQueryParameters.fromNameAndType("counts", QueryableStoreTypes.keyValueStore())
        );
        return counts.get(word);
    }

}
