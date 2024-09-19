from time import sleep

import pika
from decouple import config
from shared.logger import logging

# Configuration
BROKER_HOST = config("BROKER_HOST")
BROKER_PUB_QUEUE = config("BROKER_PUB_QUEUE")
BROKER_SUB_QUEUE = config("BROKER_SUB_QUEUE")
BROKER_USER = config("BROKER_USER")
BROKER_PASS = config("BROKER_PASS")
RETRY_ATTEMPTS = 5
RETRY_DELAY = 2  # seconds


class SyncManager:
    """
    SyncManager class is responsible for managing the connection to
    the RabbitMQ broker and handling multiple queues.
    """

    def __init__(self):
        """
        Initialize the SyncManager and connect to the RabbitMQ broker.
        """

        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        """
        Connect to the RabbitMQ broker and declare both queues.
        """

        if self.connection is None or self.connection.is_closed:
            try:
                logging.info("Connecting to RabbitMQ broker...")
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=BROKER_HOST,
                        credentials=pika.PlainCredentials(
                            username=BROKER_USER, password=BROKER_PASS
                        ),
                    )
                )
                self.channel = self.connection.channel()

                self.channel.queue_declare(
                    queue=BROKER_PUB_QUEUE, durable=True
                )
                self.channel.queue_declare(
                    queue=BROKER_SUB_QUEUE, durable=True
                )

                logging.info(
                    "Successfully connected to RabbitMQ and declared queues."
                )
            except Exception as e:
                logging.error(f"Failed to connect to RabbitMQ: {e}")

    def disconnect(self):
        """
        Disconnect from the RabbitMQ broker.
        """

        if self.connection and not self.connection.is_closed:
            try:
                self.connection.close()
                logging.info("Disconnected from RabbitMQ broker.")
            except Exception as e:
                logging.error(f"Failed to disconnect from RabbitMQ: {e}")

    def publish(self, message, queue=BROKER_PUB_QUEUE):
        """
        Publish a message to the specified RabbitMQ queue with retry logic.
        """

        if not self.connection or self.connection.is_closed:
            self.connect()

        for attempt in range(RETRY_ATTEMPTS):
            try:
                self.channel.basic_publish(
                    exchange="",
                    routing_key=queue,
                    body=message,
                    properties=pika.BasicProperties(delivery_mode=2),
                )
                logging.info(f"NEW message published to {queue}")
                break
            except Exception as e:
                logging.error(
                    f"Failed to publish message to {queue} on attempt "
                    f"{attempt + 1}: {e}"
                )
                if attempt < RETRY_ATTEMPTS - 1:
                    sleep(RETRY_DELAY)
                else:
                    logging.error(
                        f"All attempts to publish message to {queue} failed."
                    )

    def consume(self, callback, queue=BROKER_SUB_QUEUE):
        """
        Consume messages from the specified RabbitMQ queue.
        """

        if not self.connection or self.connection.is_closed:
            self.connect()

        try:
            self.channel.basic_consume(
                queue=queue, on_message_callback=callback, auto_ack=True
            )
            logging.info(f"Started consuming from queue {queue}.")
            self.channel.start_consuming()
        except Exception as e:
            logging.error(
                f"Failed to consume messages from queue {queue}: {e}"
            )
