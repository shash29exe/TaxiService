from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from keyboards.reply import income_menu_kb

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