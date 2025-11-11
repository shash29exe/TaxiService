import asyncio
from aiogram import Bot, Dispatcher
import logging

from config import TOKEN
from handlers import start
from handlers.driver import h01_income, h02_expense, h03_report

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(h01_income.router)
dp.include_router(h02_expense.router)
dp.include_router(h03_report.router)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
