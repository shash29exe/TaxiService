import asyncio
from aiogram import Bot, Dispatcher
import logging

from config import TOKEN
from handlers import start, payment
from handlers.admin import h01_summary, h02_export, h03_add_driver, h04_remove_driver
from handlers.driver import h01_income, h02_expense, h03_report
from middleware.check_driver import CheckDriverMiddleware

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.message.middleware(CheckDriverMiddleware())
dp.callback_query.middleware(CheckDriverMiddleware())

dp.include_router(start.router)
dp.include_router(payment.router)
dp.include_router(h01_income.router)
dp.include_router(h02_expense.router)
dp.include_router(h03_report.router)

dp.include_router(h01_summary.router)
dp.include_router(h02_export.router)
dp.include_router(h03_add_driver.router)
dp.include_router(h04_remove_driver.router)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
