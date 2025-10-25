from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram import F, Router

from keyboards.reply import get_id_kb, driver_menu, admin_menu, contact_admin
from utils.auth import check_admin, check_drivers

router = Router()


@router.message(F.text == '/start')
async def start(message: Message):
    """
        Реакция на команду /start.
    """

    await message.answer("Получите ваш ID", reply_markup=get_id_kb())




@router.message(F.text == 'Получить ID')
async def get_id(message: Message):
    """
        Получение ID пользователя.
    """

    user_id = message.from_user.id

    if check_admin(user_id):
        await message.answer("Привет, admin.", reply_markup=admin_menu())

    elif check_drivers(user_id):
        await message.answer("Привет, водитель.", reply_markup=driver_menu())

    else:
        tg_id = message.from_user.id
        await message.answer(f'Ваш ID: {tg_id}\nДля работы бота свяжитесь с администратором.',
                             reply_markup=contact_admin(),
                             parse_mode="Markdown"
                             )