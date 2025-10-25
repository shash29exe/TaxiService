import asyncio
from aiogram import Bot, Dispatcher
import logging

from config import TOKEN
from handlers import start


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp=Dispatcher()

dp.include_router(start.router)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
