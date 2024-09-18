async def callback(ch, method, properties, body):
    """
    Callback function to handle incoming messages from the RabbitMQ broker.
    """

    print(f"Received message: {body}")
