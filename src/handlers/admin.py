from aiogram.fsm.context import FSMContext
from loguru import logger
from src.middlewares import AdminMiddleware

from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery
)
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, StateFilter

from src.db import User, get_user

router = Router()
router.message.middleware(AdminMiddleware())


class Item(StatesGroup):
    enter_id = State()
    enter_item = State()
    enter_quantity = State()


@router.message(Command("add_recipe"))
@router.message(F.text.lower().in_(["добавить рецепт", "доб рец"]))
async def add_recipes(message: Message):
    await message.reply("<b>Рецепт успешно добавлен</b>")


@router.message(Command("add_item"))
@router.message(F.text.lower().in_(["добавить предмет", "доб пред"]))
async def add_item(message: Message, state: FSMContext):
    await message.reply("Введите id: ")
    await state.set_state(Item.enter_id)


@router.message(Item.enter_id)
async def enter_item(message: Message, state: FSMContext):
    try:
        await state.set_data({"id": int(message.text)})
    except ValueError:
        await message.reply("Вы ввели неправильный id")
        return

    if await get_user((await state.get_data())["id"]) is not None:
        await message.reply("Отлично! Теперь введите название")
        await state.set_state(Item.enter_item)
    else:
        await message.reply("Такого пользователя нет!")


@router.message(Item.enter_item)
async def enter_item(message: Message, state: FSMContext):
    user = await get_user((await state.get_data())["id"])
    if message.text in user.inventory.model_dump():
        await state.update_data({"item": message.text.lower()})
        await message.reply("Отлично! Теперь введите количество: ")
        await state.set_state(Item.enter_quantity)
    else:
        await message.reply("<b>Извините, такого аттрибута нет!</b>")


@router.message(Item.enter_quantity)
async def enter_quantity(message: Message, state: FSMContext):
    item = (await state.get_data())["item"]
    user_id = (await state.get_data())["id"]
    try:
        quantity = int(message.text)
    except ValueError:
        await message.reply("Вы ввели неправильное значение!")
        return

    user = await get_user(user_id)
    inventory = user.inventory.model_dump()
    inventory[item]["quantity"] += quantity
    user.inventory = inventory
    await user.save()
    await state.clear()
    await message.reply(f"{inventory[item]['emoji']}{inventory[item]['name']} + {quantity}")
