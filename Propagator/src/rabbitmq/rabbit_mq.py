import os

import pika
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

# RabbitMQ settings
RABBITMQ_USER = os.getenv("MAIN_MQ_DEFAULT_USER")
RABBITMQ_PASS = os.getenv("MAIN_MQ_DEFAULT_PASS")
RABBITMQ_HOST = os.getenv("MAIN_MQ_HOST")
RABBITMQ_PORT = os.getenv("MAIN_MQ_PORT")

# Initialize RabbitMQ connection
rabbitmq_credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
rabbitmq_parameters = pika.ConnectionParameters(RABBITMQ_HOST, int(RABBITMQ_PORT), '/', rabbitmq_credentials)
rabbitmq_connection = pika.BlockingConnection(rabbitmq_parameters)


def ensure_connection():
    """
    Ensure connection to Rabbit MQ.

    :return: None
    """
    if rabbitmq_connection and rabbitmq_connection.is_open:
        # TODO: Change to logging
        print("Connected to RabbitMQ")
    else:
        # TODO: Change to logging
        print("Could not connect to RabbitMQ")
