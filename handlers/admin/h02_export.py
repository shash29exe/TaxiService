import pandas as pd
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from datetime import datetime
import os

from keyboards.reply import admin_export_kb
from services.google_sheets import get_all_data

router = Router()

folder_name = 'export'
os.makedirs(folder_name, exist_ok=True)

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
        file_caption = 'день'

    elif period_text == "📆 За месяц":
        month_year = now.strftime('%m.%Y')
        df = df[df['дата'].str.endswith(month_year)]
        file_name = f'export_month_{now.strftime("%Y-%m")}.xlsx'
        file_caption = 'месяц'

    else:
        file_name = f'export_all_{now.strftime("%Y-%m-%d")}.xlsx'
        file_caption = 'всё время'

    if df.empty:
        await message.answer('Нет данных за выбранный период')
        return

    file_path = os.path.join(folder_name, file_name)

    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Все записи', index=False)

        for user, user_df in df.groupby('имя'):
            user_df.to_excel(writer, sheet_name=str(user)[:31], index=False)

        summary = (
            df.groupby('имя')['сумма']
            .apply(lambda x: pd.to_numeric(x, errors='coerce').sum())
            .reset_index()
        )

        summary.rename(columns = {'сумма': 'итоги'}, inplace = True)
        summary.to_excel(writer, sheet_name='сводка', index=False)

    await message.answer_document(FSInputFile(file_path), caption=f'Выгрузка за {file_caption}')