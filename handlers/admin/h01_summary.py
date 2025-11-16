from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.reply import admin_summary_kb, admin_menu_kb
from services.google_sheets import get_admin_summary

router = Router()

@router.message(F.text == 'Сводный отчёт')
async def admin_summary(message: Message, state: FSMContext):
    """
        Выбор периода для получения сводного отчёта.
    """

    await state.clear()
    await message.answer('Выберите период отчёта', reply_markup=admin_summary_kb())


@router.message(F.text == 'Сегодня')
async def today_summary(message: Message):
    """
        Отчёт за сегодня.
    """

    report = get_admin_summary('day')
    await message.answer(f'Отчёт за сегодня:\n {report}')


@router.message(F.text == 'За месяц')
async def month_summary(message: Message):
    """
        Отчёт за месяц.
    """

    report = get_admin_summary('month')
    await message.answer(f'Отчёт за месяц:\n {report}')


@router.message(F.text == 'За всё время')
async def all_summary(message: Message):
    """
        Отчёт за всё время.
    """

    report = get_admin_summary('all')
    await message.answer(f'Отчёт за всё время:\n {report}')


@router.message(F.text == '↩️ Назад')
async def back_to_adm_menu(message: Message, state: FSMContext):
    """
        Возврат в админское меню
    """

    await state.clear()
    await message.answer('Главное меню', reply_markup=admin_menu_kb())