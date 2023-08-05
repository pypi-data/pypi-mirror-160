import logging
import os

from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Configuration
amqp_broker = os.getenv("AMQP_BROKER")
amqp_port = os.getenv("AMQP_PORT")
amqp_user = os.getenv("AMQP_USER")
amqp_password = os.getenv("AMQP_PASSWORD")

redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")

# Endpoints for celery worker
broker_url = f"amqp://{amqp_user}:{amqp_password}@{amqp_broker}:{amqp_port}/"
result_backend = f"redis://{redis_host}:{redis_port}"

if None in [
    amqp_broker,
    amqp_port,
    amqp_user,
    amqp_password,
    redis_host,
    redis_port,
]:
    raise ValueError("Environment variables not set correctly")

# Initialize the worker
try:
    from Connector import Worker

    worker = Worker.create(
        node_name="logger-producer",
        app_name="logger producer",
        worker_queue_name="logger",
        broker_url=broker_url,  # type: ignore
        result_backend=result_backend,  # type: ignore
    )
except Exception:
    logging.exception("Cannot initialize producer")
