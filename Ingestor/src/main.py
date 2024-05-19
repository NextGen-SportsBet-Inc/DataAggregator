import threading

import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Ingestor.src.queue.consumer import RabbitMQConsumer


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
    uvicorn.run(app, host="0.0.0.0", port=8000)
