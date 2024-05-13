import threading
import uvicorn
from fastapi import FastAPI

from Ingestor.src.db.redis_database import redis_client
from Ingestor.src.queue.consumer import RabbitMQConsumer

# Run the consumer
def run_consumer(exchange, queue):
    consumer = RabbitMQConsumer(exchange, queue)
    consumer.start_consuming()

# Start consumers in threads
def start_consumers():
    
    print("start")
    
    # List of tuples (exchange, queue) for each consumer
    consumer_configs : list[tuple[str, str]]= [
        ('football', 'football_live_odds'),
    ]
    
    for exchange, queue in consumer_configs:
        thread = threading.Thread(target=run_consumer, args=(exchange, queue))
        thread.start()

# Start the consumers in a separate thread to not block the main thread
threading.Thread(target=start_consumers, daemon=True).start()

_openapi_tags = []
_description = "Microservice responsible for the data collection"

app = FastAPI(openapi_url="/api/openapi.json",
              docs_url="/api/docs",
              redoc_url="/api/redoc",
              title="Data Aggregator Ingestor API", 
              description=_description,
              openapi_tags=_openapi_tags,
              version="1.0.0",
              contact={
                  "name": "NextGen",
              },
              )

# TODO: Create a endpoint for data checkups
# @app.get("/")
# async def read_root():

if __name__ == "__main__":
    
    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)
