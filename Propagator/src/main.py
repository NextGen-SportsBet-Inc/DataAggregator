import json
import threading
import time

import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.redis_database import redis_client
from Propagator.src.queue.publisher import RabbitMQPublisher


# Run the publisher
def run_publisher(exchange, queue, routing_key):
    publisher = RabbitMQPublisher(exchange)
    publisher.declare_queue(queue=queue, routing_key=routing_key)
    
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
    
def start_publishers():
    
    # List of tuples (exchange, queue/RedisKey, routing_key) for each consumer
    consumer_configs: list[tuple[str, str, str]] = [
        ('football', 'football_live_odds', 'odds.#'),
    ]
    
    for exchange, queue, routing_key in consumer_configs:
        thread = threading.Thread(target=run_publisher, args=(exchange, queue, routing_key))
        thread.start()


# Start the consumers in a separate thread to not block the main thread
threading.Thread(target=start_publishers, daemon=True).start()

_openapi_tags = []
_description = "Microservice responsible for the data collection"

app = FastAPI(openapi_url="/api/openapi.json",
              docs_url="/api/docs",
              redoc_url="/api/redoc",
              title="Data Aggregator Propagator API",
              description=_description,
              openapi_tags=_openapi_tags,
              version="1.0.0",
              contact={
                  "name": "NextGen",
              },
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()
app.include_router(prefix="/api", router=router)


@router.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    # Run the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8001)
