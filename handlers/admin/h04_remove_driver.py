from idlelib.replace import replace

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.reply import contact_admin_kb
from services.google_sheets import add_record

router = Router()

class RemoveDriver(StatesGroup):
    """
        Удаление водителя
    """

    waiting_for_id = State()

@router.message(F.text == 'Удалить водителя')
async def ask_for_remove_driver(message: Message, state: FSMContext):
    """
        Запрос ID водителя
    """

    await state.set_state(RemoveDriver.waiting_for_id)
    await message.answer('Введите telegram ID для удаления...')


@router.message(RemoveDriver.waiting_for_id)
async def remove_driver(message: Message, state: FSMContext):
    """
        Удаление водителя
    """

    try:
        driver_id = int(message.text)

    except ValueError:
        await message.answer('Вы ввели некоректный ID.')
        return

    add_record(
        user_id=driver_id,
        username='удалённый водитель',
        record_type='водитель',
        subcategory='удаление',
        amount=0,
        comment='удаление водителя'
    )


    await message.answer(f'🗑️ Водитель с ID {driver_id} удалён')
    await message.bot.send_message(driver_id, 'Доступ запрещён.', reply_markup=contact_admin_kb())
    await state.clear()