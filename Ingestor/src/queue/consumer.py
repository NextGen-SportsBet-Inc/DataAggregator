import json
import logging
import time

from db.redis_database import redis_client
from Ingestor.src.queue.rabbit_mq import rabbitmq_connection


class RabbitMQConsumer():
    
    def __init__(self, exchange: str, queue: str):
        self.channel = rabbitmq_connection.channel()
        self.exchange = exchange
        self.queue = queue
        
        # TODO: Change to logging
        print(f'Created consumer for exchange: {exchange}, queue: {queue}')

    def start_consuming(self):

        # Make sure the exchange exists
        max_messages_in_queue = 1
        self.channel.queue_declare(queue=self.queue, durable=True, arguments={"x-max-length": max_messages_in_queue})
        
        # Configure consumption
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.on_message_callback, auto_ack=True)
        
        # Start comsuming
        # TODO: Change to logging
        print(f"Starting to consume on queue {self.queue}")
        self.channel.start_consuming()
        
    def on_message_callback(self, _, _2, _3, body):
        
        try:
            content = json.loads(body)
            
            data = {
                'timestamp': time.time(),
                'exchange': self.exchange,
                'queue': self.queue,
                'content': content
            }
            
            redis_client.set(self.queue, json.dumps(data))

            # TODO: Change to logging
            print(f"Data stored in Redis under key: {self.queue}")

        except json.JSONDecodeError as e:
            # TODO: Change to logging
            logging.error("Failed to decode JSON data: %s", e)
            
        except Exception as e:
            # TODO: Change to logging
            logging.error("Failed to store data in Redis: %s", e)
        