from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from datetime import datetime

from keyboards.reply import driver_report_select_date
from services.google_sheets import get_records_by_day, get_records_by_month

router = Router()

MONTHS = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Март',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь',
}


@router.message(F.text == 'Отчёт')
async def report_menu(message: Message, state: FSMContext):
    """
        Реакция на кнопку отчёт
    """

    await state.clear()
    await message.answer('Выберите отчёт за определённый период', reply_markup=driver_report_select_date())


@router.message(F.text == 'Текущий день')
async def daily_report(message: Message):
    """
        Отчёт за день.
    """

    telegram_id = message.from_user.id
    today = datetime.now().strftime('%d.%m.%Y')

    records = get_records_by_day(telegram_id, today)
    if not records:
        await message.answer('За текущий день отчёта нет.')
        return

    text_lines = [f'Отчёт за {today}']
    total_income = total_expense = 0

    for record in records:
        time, rec_type, category, amount, comment = record[1], record[2], record[3], record[4], record[5]
        line = f'{time}: {rec_type.upper()} - ({category}) - {amount}₽'

        if comment:
            line+= f' - {comment}'

        text_lines.append(line)

        try:
            amt = float(amount.replace(',', '.'))
            if rec_type == 'доход':
                total_income += amt

            elif rec_type == 'расход':
                total_expense += amt

        except ValueError:
            pass

    text_lines.append(f'\nОбщий доход: {total_income:.2f}₽')
    text_lines.append(f'\nОбщий расход: {total_expense:.2f}₽')
    text_lines.append(f'\nПрибыль {total_income - total_expense:.2f}')

    await message.answer('\n'.join(text_lines))


@router.message(F.text == 'За месяц')
async def month_report(message: Message):
    """
        Отчёт за месяц.
    """

    now = datetime.now()
    user_id = message.from_user.id

    records = get_records_by_month(user_id=user_id, month=now.month, year=now.year)

    if not records:
        await message.answer('За выбранный месяц отчётов нет.')
        return

    total_income = sum(float(r[4]) for r in records if r[2].lower() == 'доход')
    total_expense = sum(float(r[4]) for r in records if r[2].lower() == 'расход')

    await message.answer(
        f'Отчёт за {MONTHS[now.month].lower()} {now.year}\n'
        f'\nОбщий доход: {total_income:.2f}₽'
        f'\nОбщий расход: {total_expense:.2f}₽'
        f'\nПрибыль {total_income - total_expense:.2f}'
    )