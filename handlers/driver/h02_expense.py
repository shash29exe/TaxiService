from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from keyboards.reply import back_button_kb, driver_menu_kb
from services.google_sheets import add_record

router = Router()


class ExpenseStates(StatesGroup):
    """
        Ожидание суммы и комментария
    """

    waiting_for_amount_and_comment = State()


@router.message(F.text == "Расход")
async def start_expense(message: Message, state: FSMContext):
    """
        Реакция на кнопку расход.
    """

    await message.answer('Введите сумму и комментарий\nПример: `500.00 мойка`', reply_markup=back_button_kb(),
                         parse_mode='Markdown')
    await state.set_state(ExpenseStates.waiting_for_amount_and_comment)


@router.message(F.text == 'Назад 🔙', ExpenseStates.waiting_for_amount_and_comment)
async def clear_state_and_back(message: Message, state: FSMContext):
    """
        Возврат на шаг назад.
    """
    await state.clear()
    await message.answer('Возврат в главное меню', reply_markup=driver_menu_kb())


@router.message(ExpenseStates.waiting_for_amount_and_comment)
async def get_expense(message: Message, state: FSMContext):
    text = message.text.strip()
    parts = text.split(' ', 1)
    try:
        amount = float(parts[0].replace(',', '.'))
        comment = parts[1] if len(parts) > 1 else ''

        add_record(
            user_id=message.from_user.id,
            username=message.from_user.full_name,
            record_type='расход',
            subcategory='-',
            amount=amount,
            comment=comment
        )
        
        await message.answer(f'Расход сохранён.\nСумма: {amount}, комментарий: {comment}')
        await state.clear()
    
    except ValueError:
        await message.answer('Некорректный ввод, повторите попытку\nПример: `500.00 мойка`')