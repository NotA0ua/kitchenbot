from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from src.__init__ import admins


class AdminMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if event.from_user.id in admins:
            return await handler(event, data)

        await event.answer(
            "<b>Вы не можете использовать эту команду 😡</b>"
        )
        return
