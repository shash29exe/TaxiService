import pandas as pd
from aiogram import Router, F
from aiogram.types import Message, FSInputFile, ReplyKeyboardRemove
from datetime import datetime

from keyboards.reply import admin_menu_kb, admin_export_kb
from services.google_sheets import get_all_data

router = Router()


@router.message(F.text == "Выгрузка")
async def export_menu(message: Message):
    """
        Меню экспорта
    """

    await message.answer('Выберите период для выгрузки', reply_markup=admin_export_kb())


@router.message(F.text.in_(["📆 За день", "📆 За месяц", "📆 За всё время"]))
async def export_period(message: Message):
    """
        Выгрузка данных за определённый период
    """

    all_data = get_all_data()

    columns = [col.strip().lower() for col in all_data[0]]
    df = pd.DataFrame(all_data[1:], columns=columns)

    now = datetime.now()
    period_text = message.text

    if period_text == "📆 За день":
        df = df[df['дата'] == now.strftime('%d.%m.%Y')]
        file_name = f'export_day_{now.strftime("%Y-%m-%d")}.xlsx'