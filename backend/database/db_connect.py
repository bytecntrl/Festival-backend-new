from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from backend.config import Session


def init_db(app: FastAPI):
    conf = Session.config

    register_tortoise(
        app,
        config={
            "connections": {
                "default": {
                    "engine": "tortoise.backends.asyncpg",
                    "credentials": {
                        "host": conf.HOST,
                        "port": conf.PORT,
                        "user": conf.DB_USERNAME,
                        "password": conf.PASSWORD,
                        "database": conf.DB_NAME,
                    },
                }
            },
            "apps": {
                "models": {
                    "models": [
                        "backend.database.models.users",
                    ],
                    "default_connection": "default",
                }
            },
            "timezone": "Europe/Rome",
        },
        generate_schemas=True,
    )
