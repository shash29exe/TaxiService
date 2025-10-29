from aiogram.types import Message
from aiogram import F, Router

from keyboards.reply import get_id_kb, driver_menu_kb, admin_menu_kb, contact_admin_kb
from utils.auth import check_admin, check_drivers, get_admin_id

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
        await message.answer("Привет, admin.", reply_markup=admin_menu_kb())

    elif check_drivers(user_id):
        await message.answer("Привет, водитель.", reply_markup=driver_menu_kb())

    else:
        tg_id = message.from_user.id
        await message.answer(f'Ваш ID: {tg_id}\nДля работы бота свяжитесь с администратором.',
                             reply_markup=contact_admin_kb(),
                             parse_mode="Markdown"
                             )


@router.message(F.text == '💬 Связаться с менеджером')
async def contact_admin(message: Message):
    """
        Связь с менеджером
    """

    username = message.from_user.username
    user_id = message.from_user.id

    admin_message = (
        f'🔔 Вам пришло уведомление\n'
        f'👤 От: {username}\n'
        f'🆔 ID: {user_id}\n'
        f'🕑 Дата и время: {message.date.strftime("%d/%m/%Y %H:%M")}\n'
    )

    admin_id = get_admin_id()

    await message.bot.send_message(admin_id, admin_message)
    await message.answer('📨 Ваше сообщение отправленно администратору, ожидайте обратную связь.')