from loguru import logger

from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery
)
from aiogram.filters import Command

from src.db import User, get_user


router = Router()


@router.message(Command("start"))
async def start_cmd(message: Message):
    if not await get_user(message.from_user.id):
        user = User(
            user_id=message.from_user.id
        )
        await user.insert()
        
    await message.reply("<b>Привет!</b>")
