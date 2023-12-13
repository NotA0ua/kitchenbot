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
    enter_id_add = State()
    enter_id_set = State()

    enter_item_add = State()
    enter_item_set = State()

    enter_quantity_add = State()
    enter_quantity_set = State()


@router.message(Command("add_recipe"))
@router.message(F.text.lower().in_(["добавить рецепт", "доб рец"]))
async def add_recipes(message: Message):
    await message.reply("<b>Рецепт успешно добавлен</b>")


@router.message(Command("set_item"))
@router.message(F.text.lower().in_(["установить предмет", "уст пред"]))
async def set_item(message: Message, state: FSMContext):
    await message.reply("Введите id пользователя: ")
    await state.set_state(Item.enter_id_set)


@router.message(Command("add_item"))
@router.message(F.text.lower().in_(["добавить предмет", "доб пред"]))
async def add_item(message: Message, state: FSMContext):
    await message.reply("Введите id пользователя: ")
    await state.set_state(Item.enter_id_add)


@router.message(Item.enter_id_add)
@router.message(Item.enter_id_set)
async def enter_item(message: Message, state: FSMContext):
    if message.text.lower() != "я":
        try:
            await state.set_data({"id": int(message.text)})
        except ValueError:
            await message.reply("Вы ввели неправильный id пользователя ❌")
            return
    else:
        await state.set_data({"id": message.from_user.id})

    if await get_user((await state.get_data())["id"]) is not None:
        await state.set_state(Item.enter_item_add if await state.get_state() == Item.enter_id_add
                              else Item.enter_item_set)
        await message.reply("Отлично! Теперь введите название: ")
    else:
        await message.reply("Такого пользователя нет! ❌")


@router.message(Item.enter_item_add)
@router.message(Item.enter_item_set)
async def enter_item(message: Message, state: FSMContext):
    user = await get_user((await state.get_data())["id"])
    if message.text in user.inventory.model_dump():
        await state.update_data({"item": message.text.lower()})
        await state.set_state(
            Item.enter_quantity_add if await state.get_state() == Item.enter_item_add else Item.enter_quantity_set)
        await message.reply("Отлично! Теперь введите количество: ")
    else:
        await message.reply("<b>Извините, такого аттрибута нет! ❌</b>")


@router.message(Item.enter_quantity_add)
@router.message(Item.enter_quantity_set)
async def enter_quantity(message: Message, state: FSMContext):
    item = (await state.get_data())["item"]
    user_id = (await state.get_data())["id"]
    try:
        quantity = int(message.text)
    except ValueError:
        await message.reply("Вы ввели неправильное значение! ❌")
        return

    user = await get_user(user_id)
    inventory = user.inventory.model_dump()
    if await state.get_state() == Item.enter_quantity_add:
        inventory[item]["quantity"] += quantity
        await message.reply(f"<b>{inventory[item]['emoji']} <code>{inventory[item]['name']}</code> + {quantity}</b>\n"
                            f"<b>Теперь {inventory[item]['quantity']}</b>")
    else:
        inventory[item]["quantity"] = quantity
        await message.reply(
            f"<b>{inventory[item]['emoji']}<code>{inventory[item]['name']} </code> - теперь {quantity}</b>")

    user.inventory = inventory
    await user.save()
    await state.clear()
