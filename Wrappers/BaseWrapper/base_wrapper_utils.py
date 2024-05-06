import os
from dotenv import load_dotenv
from enum import Enum

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
        self._rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER")
        self._rabbitmq_pass = os.getenv("RABBITMQ_DEFAULT_PASS")
        self._rabbitmq_host = os.getenv("RABBITMQ_HOST")
        self._rabbitmq_port = os.getenv("RABBITMQ_PORT")

        # RAPID API
        self.sport = sport.name
        self._api_key = sport.value
        self._api_host = os.getenv("API_HOST")
        self._api_request_headers = {
            "X-RapidAPI-Key": self._api_key,
            "X-RapidAPI-Host": self._api_host
        }

    def init_client(self):
        from pika import PlainCredentials, ConnectionParameters, BlockingConnection

        rabbitmq_credentials = PlainCredentials(self._rabbitmq_user, self._rabbitmq_pass)
        rabbitmq_parameters = ConnectionParameters(self._rabbitmq_host, int(self._rabbitmq_port), '/', rabbitmq_credentials)
        rabbitmq_connection = BlockingConnection(rabbitmq_parameters)
        self._rabbitmq_channel = rabbitmq_connection.channel()

    def exchange_declare(self, exchange: str):
        if not self._rabbitmq_channel:
            raise ValueError("RabbitMQ channel is not initialized. Call init_client() first.")

        self._exchange = exchange
        self._rabbitmq_channel.exchange_declare(exchange=exchange, exchange_type='topic')

    def publish_to(self, message: str):
        if not self._exchange:
            raise ValueError(
                "RabbitMQ channel exchange is not declared. Call exchange_declare() first, passing the exchange.")

        # Publish the message to the specified topic
        self._rabbitmq_channel.basic_publish(
            exchange=self._exchange,
            routing_key='',  # Routing key is set to the empty string for topic exchange
            body=message
        )

        print(f"\tSent message to topic '{self._exchange}': {message}")  # TODO: Change to logging

    def call_api(self, url: str):
        import requests

        url = f"https://{self._api_host}/{url}"

        print(f"\tCall API: {url}")  # TODO: Simplify this step, log and pass the url to the request get

        response = requests.get(url, headers=self._api_request_headers)
        return response.json()
