import threading

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from modules.book.router import book_router
from modules.user.router import user_router
from shared.broker import SyncManager
from shared.error_handler import CustomError
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


@app.exception_handler(CustomError)
async def custom_error_handler(request: Request, exc: CustomError):
    return JSONResponse(
        status_code=exc.http_status_code,
        content={"error": exc.message},
    )


@app.exception_handler(RequestValidationError)
async def handle_validation_error(request, exc):
    """
    Handle validation errors
    """

    first_error = exc.errors()[0]
    error_msg = first_error.get("msg")
    error_loc = first_error.get("loc")

    return JSONResponse(
        status_code=422,
        content={"error": error_msg + " : " + error_loc[1]},
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
