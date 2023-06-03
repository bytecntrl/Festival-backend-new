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
                        "backend.database.models.ingredient_order",
                        "backend.database.models.ingredients",
                        "backend.database.models.menu",
                        "backend.database.models.menu_product",
                        "backend.database.models.menu_validity",
                        "backend.database.models.orders",
                        "backend.database.models.product_order",
                        "backend.database.models.product_validity",
                        "backend.database.models.products",
                        "backend.database.models.role_menu",
                        "backend.database.models.role_product",
                        "backend.database.models.subcategories",
                        "backend.database.models.users",
                        "backend.database.models.variant",
                    ],
                    "default_connection": "default",
                }
            },
            "timezone": "Europe/Rome",
        },
        generate_schemas=True,
    )
