import json
import os
from enum import Enum
from typing import Any

from dotenv import load_dotenv

load_dotenv(".env")


class SportKey(Enum):
    BASEBALL = os.getenv("BASEBALL_API_KEY")
    BASKETBALL = os.getenv("BASKETBALL_API_KEY")
    HOCKEY = os.getenv("HOCKEY_API_KEY")
    FOOTBALL = os.getenv("FOOTBALL_API_KEY")


class BaseWrapperUtils:
    def __init__(self, sport: SportKey):
        
        # RabbitMQ
        self._exchange = None
        self._rabbitmq_channel = None
        self._rabbitmq_user = os.getenv("WRAPPERS_MQ_DEFAULT_USER")
        self._rabbitmq_pass = os.getenv("WRAPPERS_MQ_DEFAULT_PASS")
        self._rabbitmq_host = os.getenv("WRAPPERS_MQ_HOST")
        self._rabbitmq_port = os.getenv("WRAPPERS_MQ_PORT")

        # RAPID API
        self.sport = sport.name
        self._api_key = sport.value
        self._api_host = os.getenv("API_HOST")
        self._api_request_headers = {
            "X-RapidAPI-Key": self._api_key,
            "X-RapidAPI-Host": self._api_host
        }

    def init_client(self):
        from pika import (BlockingConnection, ConnectionParameters,
                          PlainCredentials)

        rabbitmq_credentials = PlainCredentials(self._rabbitmq_user, self._rabbitmq_pass)
        rabbitmq_parameters = ConnectionParameters(self._rabbitmq_host, int(self._rabbitmq_port), '/', rabbitmq_credentials)
        rabbitmq_connection = BlockingConnection(rabbitmq_parameters)
        self._rabbitmq_channel = rabbitmq_connection.channel()

    def exchange_declare(self, exchange: str):
        if not self._rabbitmq_channel:
            raise ValueError("RabbitMQ channel is not initialized. Call init_client() first.")

        self._exchange = exchange
        self._rabbitmq_channel.exchange_declare(exchange=self._exchange, exchange_type='topic')
        
    def declare_queue(self, queue: str, routing_key: str):
        if not self._rabbitmq_channel:
            raise ValueError("RabbitMQ channel exchange is not declared. Call exchange_declare() first, passing the exchange.")
        
        # Declare the queue for publishing a limited number of messages
        max_messages_in_queue = 1
        self._rabbitmq_channel.queue_declare(queue=queue, durable=True, arguments={"x-max-length": max_messages_in_queue})
        
        # Bind the queue to the exchange with the routing key
        self._rabbitmq_channel.queue_bind(exchange=self._exchange, queue=queue, routing_key=routing_key)

        # TODO: Change to logging
        print(f"Queue '{queue}' declared and bound to exchange '{self._exchange}' with routing key '{routing_key}'")

    def publish_to(self, message: Any, routing_key: str = ''):
        if not self._exchange:
            raise ValueError("RabbitMQ channel exchange is not declared. Call exchange_declare() first, passing the exchange.")
        
        # Converts the dictionary (message) to a JSON string
        message_bytes = json.dumps(message).encode('utf-8')

        self._rabbitmq_channel.basic_publish(
            exchange=self._exchange,
            routing_key=routing_key,
            body=message_bytes
        )

        # TODO: Change to logging
        print(f"Sent message to topic '{self._exchange}'")

    def call_api(self, url: str):
        import requests

        url = f"https://{self._api_host}/{url}"

        # TODO: Change to logging
        print(f"Call API: {url}")  # TODO: Simplify this step and pass the url to the request get

        response = requests.get(url, headers=self._api_request_headers)
        return response.json()
