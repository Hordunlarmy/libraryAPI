from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules.book.router import book_router
from modules.user.router import user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "This is the backend API"}


app.include_router(user_router)
app.include_router(book_router)
