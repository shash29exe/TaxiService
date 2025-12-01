from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

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

    tg_id = message.text
    print(tg_id)

    """
        TODO: доделать удаление из гугл таблиц.
    """

    await message.answer(f'🗑️ Водитель с ID {tg_id} удалён')
    await state.clear()