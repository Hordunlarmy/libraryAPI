import threading

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.book.router import book_router
from modules.user.router import user_router
from shared.broker import SyncManager
from shared.logger import logging
from shared.utils import callback
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RabbitMQMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)
        self.consumer_started = False
        self.sync_manager = SyncManager()

    async def dispatch(self, request, call_next):
        if not self.consumer_started or not self.sync_manager.is_connected():
            if not self.sync_manager.is_connected():
                logging.warning("RabbitMQ connection lost, reconnecting...")
                self.sync_manager.reconnect()

            logging.info("Starting or restarting RabbitMQ consumer...")
            consumer_thread = threading.Thread(
                target=self.sync_manager.consume, args=(callback,)
            )
            consumer_thread.start()
            self.consumer_started = True
            logging.info("RabbitMQ consumer started")
        else:
            logging.info("RabbitMQ consumer is already running")

        response = await call_next(request)
        return response


app.add_middleware(RabbitMQMiddleware)


@app.get("/")
def read_root():
    return {"Hello": "This is the backend API"}


app.include_router(user_router)
app.include_router(book_router)
