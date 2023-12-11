from aiogram import Router
from . import basic

def connect_routers() -> Router:
    router = Router()
    router.include_routers(
        basic.router,
    )
    
    return router