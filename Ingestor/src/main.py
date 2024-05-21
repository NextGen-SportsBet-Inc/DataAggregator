import threading

from rabbitmq.consumer import RabbitMQConsumer


# Run the consumer
def run_consumer(exchange, queue):
    consumer = RabbitMQConsumer(exchange, queue)
    consumer.start_consuming()


# Start consumers in threads
def main():
    # List of tuples (exchange, queue/RedisKey) for each consumer
    consumer_configs: list[tuple[str, str]] = [
        ('football', 'football_live_odds'),
    ]

    for exchange, queue in consumer_configs:
        thread = threading.Thread(target=run_consumer, args=(exchange, queue))
        thread.start()


if __name__ == "__main__":
    main()
