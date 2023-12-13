from aiogram.fsm.context import FSMContext
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
async def start_cmd(message: Message, state: FSMContext):
    if not await get_user(message.from_user.id):
        user = User(
            user_id=message.from_user.id
        )
        await user.insert()

    await state.clear()
    await message.reply("<b>Привет, я кухонный бот!</b>")


@router.message(Command("inventory"))
@router.message(F.text.lower().in_(["инв", "инвентарь"]))
async def inventory_cmd(message: Message):
    user_id = message.from_user.id
    user = await get_user(user_id)

    text = "<i><b>Твой инвентарь:</b></i>\n\n"
    for key, item in user.inventory.model_dump().items():
        text += f"{item['emoji']} {item['name']} - {item['quantity']}\n" if item['quantity'] > 0 else ""

    await message.reply(text)
