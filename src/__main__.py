import asyncio
import os
import dotenv

from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

dotenv.load_dotenv()


async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    
    logger.info("Starting bot")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())