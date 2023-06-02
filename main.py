from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config import Config, Session
from backend.database import init_db
from backend.responses.error import UnicornException
from backend.routers import auth

app = FastAPI()


# env
load_dotenv()


# config
conf = Session.config = Config()


# CORS
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# routers
app.include_router(auth.router)


# db
init_db(app)


# error
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(_: Request, exc: UnicornException):
    return JSONResponse(
        status_code=exc.status, content={"error": True, "message": exc.message}
    )
