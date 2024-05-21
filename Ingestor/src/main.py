import threading

from queue.consumer import RabbitMQConsumer


# Run the consumer
def run_consumer(exchange, queue):
    consumer = RabbitMQConsumer(exchange, queue)
    consumer.start_consuming()


# Start consumers in threads
def start_consumers():
    # List of tuples (exchange, queue/RedisKey) for each consumer
    consumer_configs: list[tuple[str, str]] = [
        ('football', 'football_live_odds'),
    ]

    for exchange, queue in consumer_configs:
        thread = threading.Thread(target=run_consumer, args=(exchange, queue))
        thread.start()


def main():
    # Start the consumers in a separate thread to not block the main thread
    threading.Thread(target=start_consumers, daemon=True).start()


if __name__ == "__main__":
    main()
