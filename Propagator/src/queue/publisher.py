import json
import pika

from Propagator.src.queue.rabbit_mq import rabbitmq_connection


class RabbitMQPublisher():
    
    def __init__(self, exchange: str):
        self._channel = rabbitmq_connection.channel()
        self._exchange = exchange
        
        self._channel.exchange_declare(exchange=self._exchange, exchange_type='topic')
        
        # TODO: Change to logging
        print(f'Created publisher for exchange: {exchange}')
        
    def declare_queue(self, queue: str, routing_key: str):
        # Declare the queue for publishing a limited number of messages
        max_messages_in_queue = 1
        self._channel.queue_declare(queue=queue, durable=True, arguments={"x-max-length": max_messages_in_queue})
        
        # Bind the queue to the exchange with the routing key
        self._channel.queue_bind(exchange=self._exchange, queue=queue, routing_key=routing_key)

        # TODO: Change to logging
        print(f"Queue '{queue}' declared and bound to exchange '{self._exchange}' with routing key '{routing_key}'")
        
    def publish_message(self, message: str, routing_key: str = ''):
        
        # Converts the dictionary (message) to a JSON string
        message_bytes = json.dumps(message).encode('utf-8')

        self._channel.basic_publish(
            exchange=self._exchange,
            routing_key=routing_key,
            body=message_bytes,
            properties=pika.BasicProperties(
                delivery_mode=2,  # TODO: Change if we don't want presistency
            )
        )

        # TODO: Change to logging
        print(f"Sent message to topic '{self._exchange}'")