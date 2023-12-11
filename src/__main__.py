import asyncio
import os
import dotenv

from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from src.handlers import connect_routers

from src.db import User
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

dotenv.load_dotenv()


async def main():
    logger.info("Initializing MongoDB")
    mongo = AsyncIOMotorClient(os.getenv("MONGO_URL"))
    await init_beanie(database=mongo.kitchenbot, document_models=[User])
    
    bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    
    routers = connect_routers()
    dp.include_router(routers)
    dp.startup.register(startup)
    
    logger.info("Starting bot")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def startup():
    logger.info("Bot successfully started!")

if __name__ == "__main__":
    asyncio.run(main())