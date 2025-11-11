from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from keyboards.reply import income_menu_kb, back_button_kb, driver_menu_kb
from services.google_sheets import add_record

router = Router()


class IncomeStates(StatesGroup):
    choosing_type = State()
    waiting_for_amount = State()
    waiting_for_comment = State()


@router.message(F.text == 'Доход')
async def show_income_menu(message: Message, state: FSMContext):
    """
        Расчет доходов.
    """

    await message.answer('Выберите тип дохода', reply_markup=income_menu_kb())
    await state.set_state(IncomeStates.choosing_type)


@router.message(IncomeStates.choosing_type, F.text.in_(['Оплата за заказ', 'Доплата за заказ']))
async def ask_income_amount(message: Message, state: FSMContext):
    """
        Запрос суммы дохода
    """

    await state.update_data(income_type=message.text)
    await message.answer('Введите сумму числом\nПример: `300.00`', parse_mode='Markdown', reply_markup=back_button_kb())
    await state.set_state(IncomeStates.waiting_for_amount)


@router.message(IncomeStates.waiting_for_amount)
async def ask_income_comment(message: Message, state: FSMContext):
    """
        Запрос коментария
    """

    if message.text == 'Назад 🔙':
        await state.set_state(IncomeStates.choosing_type)
        await message.answer('Выберите тип дохода', reply_markup=income_menu_kb())

        return

    try:
        amount = float(message.text.replace(',', '.'))

    except ValueError:
        await message.answer('Введите корректную сумму.')
        return

    await state.update_data(amount=amount)
    await message.answer('Добавьте коментарий\nПример:\n`Адрес заказа: Просп. Победы 01`', parse_mode='Markdown',
                         reply_markup=back_button_kb())
    await state.set_state(IncomeStates.waiting_for_comment)


@router.message(IncomeStates.waiting_for_comment)
async def confirm_income(message: Message, state: FSMContext):
    """
        Подтверждение доходов.
    """

    user_data = await state.get_data()
    income_type = user_data['income_type']
    amount = user_data['amount']
    comment = message.text

    subcategory = 'оплата' if income_type == 'Оплата за заказ' else 'доплата'

    add_record(
        user_id=message.from_user.id,
        username=message.from_user.full_name,
        record_type='доход',
        subcategory=subcategory,
        amount=amount,
        comment=comment
    )

    await message.answer(
        f'Доход зарегистрирован\nТип дохода: {income_type}\nСумма: {amount:.2f}₽\nКоментарий: {comment}',
        reply_markup=income_menu_kb()
    )

    await state.clear()


@router.message(F.text == 'Назад 🔙')
async def back_one_step(message: Message, state: FSMContext):
    """
        Возврат в меню дохода.
    """

    await state.clear()
    await message.answer('Выберите тип дохода', reply_markup=income_menu_kb())


@router.message(F.text == '🔙 Назад')
async def clear_state_and_back(message: Message, state: FSMContext):
    """
        Возврат на шаг назад.
    """
    await state.clear()
    await message.answer('Главное меню', reply_markup=driver_menu_kb())