import json
import threading
import time

from rabbitmq.publisher import RabbitMQPublisher
from db.redis_database import redis_client

print("Propagator started")

# Run the publisher
def run_publisher(exchange, queue, routing_key):
    publisher = RabbitMQPublisher(exchange)
    publisher.declare_queue(queue=queue, routing_key=routing_key)
    
    print(f"Started publisher for exchange: {exchange}, queue: {queue}, routing_key: {routing_key}")

    last_value = None
    while True:
        try:
            current_value = json.loads(redis_client.get(queue))

            if current_value != last_value:
                # TODO: Change to logging
                print(f"Value for {queue} changed")

                publisher.publish_message(current_value, routing_key)
                last_value = current_value

            time.sleep(1)  # Check every second

        except Exception as e:
            # TODO: Change to logging
            print(f"Error monitoring Redis key: {e}")
            break


# Start the consumers in a separate thread to not block the main thread
def main():
    # List of tuples (exchange, queue/RedisKey, routing_key) for each consumer
    consumer_configs: list[tuple[str, str, str]] = [
        ('football', 'football_live_odds', 'odds.#'),
    ]

    for exchange, queue, routing_key in consumer_configs:        
        thread = threading.Thread(target=run_publisher, args=(exchange, queue, routing_key))
        thread.start()


if __name__ == "__main__":
    main()
