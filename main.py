import secrets
import string
import sys

from argon2 import PasswordHasher
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from backend.config import Config, Session
from backend.database import init_db
from backend.database.models import Users
from backend.responses.error import UnicornException
from backend.routers import auth, products, roles, subcategories, users

FMT = "<green>[{time}]</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

# logger
logger.configure(
    handlers=[
        {"sink": sys.stdout, "format": FMT},
        {"sink": "log.log", "format": FMT},
    ]
)

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
app.include_router(products.router)
app.include_router(roles.router)
app.include_router(subcategories.router)
app.include_router(users.router)


# db
init_db(app)


# error
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(_: Request, exc: UnicornException):
    return JSONResponse(
        status_code=exc.status, content={"error": True, "message": exc.message}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _: Request, exc: RequestValidationError
):
    detail = exc.errors()

    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "message": "Request Validation Error",
            "detail": detail,
        },
    )


# creation admin user if not exist
@app.on_event("startup")
async def startup_event():
    if not await Users.filter(role="admin").exists():
        alphabet = string.ascii_letters + string.digits
        password = "".join(secrets.choice(alphabet) for _ in range(8))

        ph = PasswordHasher()

        await Users(
            username="admin", password=ph.hash(password), role="admin"
        ).save()

        logger.info(f"Created the admin user with password {password}")
