from loguru import logger
from src.__init__ import admins


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
        
    await message.reply("<b>Привет, я кухонный бот!</b>")


@router.message(Command("add_recipe"))
async def add_recipes(message: Message):
    if message.from_user.id in admins:
        await message.reply("<b>Рецепт успешно добавлен</b>")
    else:
        await message.reply("<b>У вас нет прав использовать эту команду!</b>")

# @router.message(Command("recipes"))
# async def recipes_cmd(message: Message):
