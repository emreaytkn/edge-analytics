package com.edge.analytics.controller;

import com.edge.analytics.kafka.MessageProducer;
import com.edge.analytics.schema.CmapssInferenceResult;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AllArgsConstructor;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StoreQueryParameters;
import org.apache.kafka.streams.state.QueryableStoreTypes;
import org.apache.kafka.streams.state.ReadOnlyKeyValueStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.config.StreamsBuilderFactoryBean;
import org.springframework.web.bind.annotation.*;

import java.util.*;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api")
public class KafkaController {

    @Autowired
    private final StreamsBuilderFactoryBean factoryBean;

    @Autowired
    private MessageProducer messageProducer;

    // Experimental purposes - Ideally store in a db
    // TODO: Deserialize Kafka message to object
    //private List<CmapssInferenceResult> messageList = new ArrayList<>();

    private List<CmapssInferenceResult> messageList = new ArrayList<>();

    public KafkaController(StreamsBuilderFactoryBean factoryBean) {
        this.factoryBean = factoryBean;
    }

    @KafkaListener(topics = "cmapss-output", groupId = "test-group-id")
    public void listenAndAddMsg(String message) throws JsonProcessingException {
        System.out.println("Adding to list: " + message);
        ObjectMapper mapper = new ObjectMapper();
        CmapssInferenceResult cmapssInferenceResult = mapper.readValue(message, CmapssInferenceResult.class);
        messageList.add(cmapssInferenceResult);
    }

    @GetMapping("/kafka/cmapss/experiments")
    @ResponseBody
    public List<CmapssInferenceResult> filterMessages() {

        // TODO: Filter by experimentId. Currently returning all the experiment results
        return messageList;
    }

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
