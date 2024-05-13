
import json
import logging
from Ingestor.src.queue.rabbit_mq import rabbitmq_connection
from Ingestor.src.db.redis_database import redis_client


class RabbitMQConsumer():
    
    def __init__(self, exchange: str, queue: str):
        self.channel = rabbitmq_connection.channel()
        self.exchange = exchange
        self.queue = queue
        
        print(f'Created consumer for exchange: {exchange}, queue: {queue}')

    def start_consuming(self):

        # Make sure the exchange exists
        max_messages_in_queue = 1
        self.channel.queue_declare(queue=self.queue, durable=True, arguments={"x-max-length": max_messages_in_queue})
        
        # Configure consumption
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.on_message_callback, auto_ack=True)
        
        # Start comsuming
        print(f"Starting to consume on queue {self.queue}")
        self.channel.start_consuming()
        
    def on_message_callback(self, ch, method, properties, body):
        """Callback function that handles message processing and storing data into Redis."""
        try:
            data = json.loads(body)
            print(f"Received message from {self.exchange}: {data}")

            redis_client.set(self.queue, json.dumps(data))

            print(f"Data stored in Redis under key: {self.queue}")
        except json.JSONDecodeError as e:
            logging.error("Failed to decode JSON data: %s", e)
        except Exception as e:
            logging.error("Failed to store data in Redis: %s", e)
        