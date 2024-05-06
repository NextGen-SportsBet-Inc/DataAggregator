import json
import uvicorn
from fastapi import (FastAPI,
                     BackgroundTasks)
from Ingestor.src.db.redis_database import redis_client
from Ingestor.src.queue.rabbit_mq import rabbitmq_connection

_openapi_tags = []
_description = "Microservice responsible for the data collection"

app = FastAPI(openapi_url="/api/openapi.json",
              docs_url="/api/docs",
              redoc_url="/api/redoc",
              title="Data Aggregator API",
              description=_description,
              openapi_tags=_openapi_tags,
              version="1.0.0",
              contact={
                  "name": "NextGen",
              }
              )


# Function to store data in Redis
def store_data_in_redis(key, value):
    if not redis_client.exists(key):
        redis_client.set(key, value)


# Function to process RabbitMQ messages
def rabbitmq_consumer():
    channel = rabbitmq_connection.channel()
    channel.queue_declare(queue='data_queue')

    # def callback(ch, method, properties, body):
    def callback(_, _2, _3, body):
        data = json.loads(body)
        store_data_in_redis(data['key'], data['value'])

    channel.basic_consume(queue='data_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


@app.on_event("startup")
async def startup_event(background_tasks: BackgroundTasks):
    # Add the RabbitMQ consumer as a background task
    background_tasks.add_task(rabbitmq_consumer)

    # TODO: Create a background task to compare and queue the new data


# TODO: Create a endpoint for data checkups
# @app.get("/")
# async def read_root():


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
