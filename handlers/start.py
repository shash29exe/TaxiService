from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram import F, Router

from keyboards.reply import get_id

router = Router()

@router.message(F.text=='/start')
async def start(message: Message):
    """
        Реакция на команду /start.
    """

    await message.answer("Получите ваш ID", reply_markup=get_id())