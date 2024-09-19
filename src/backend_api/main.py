from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.book.router import book_router
from modules.user.router import user_router
import threading
from shared.logger import logging
from starlette.middleware.base import BaseHTTPMiddleware
from shared.broker import SyncManager
from shared.utils import callback


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

    async def dispatch(self, request, call_next):
        if not self.consumer_started:
            logging.info("Starting RabbitMQ consumer...")
            consumer_thread = threading.Thread(
                target=SyncManager().consume, args=(callback,)
            )
            consumer_thread.start()
            self.consumer_started = True
            logging.info("RabbitMQ consumer started")
        else:
            logging.info("RabbitMQ consumer already running")

        response = await call_next(request)
        return response


app.add_middleware(RabbitMQMiddleware)


@app.get("/")
def read_root():
    return {"Hello": "This is the backend API"}


app.include_router(user_router)
app.include_router(book_router)
