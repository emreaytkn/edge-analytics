package com.edge.analytics.controller;

import com.edge.analytics.kafka.MessageProducer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class KafkaController {

    @Autowired
    private MessageProducer messageProducer;

    @PostMapping("/kafka/test")
    public String sendMessage(@RequestBody String message) {
        messageProducer.sendMessage(message);
        return "Message sent: " + message;
    }

}
