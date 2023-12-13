from aiogram import Router
from . import basic
from . import admin


def connect_routers() -> Router:
    router = Router()
    router.include_routers(
        basic.router,
        admin.router
    )

    return router
