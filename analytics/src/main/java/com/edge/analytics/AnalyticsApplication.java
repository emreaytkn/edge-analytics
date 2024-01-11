package com.edge.analytics;

import org.apache.kafka.common.protocol.types.Field;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.support.SendResult;

import java.util.concurrent.CompletableFuture;

@SpringBootApplication
public class AnalyticsApplication {

	public static void main(String[] args) {
		SpringApplication.run(AnalyticsApplication.class, args);
	}



	@Bean
	public MessageListener messageListener() {
		return new MessageListener();
	}


	public static class MessageListener {

		@KafkaListener(topics = "${message.topic.name}", groupId = "foo")
		public void listenGroupFoo(String message) {
			System.out.println("Received message in group 'foo' : " + message);
		}
	}

}
