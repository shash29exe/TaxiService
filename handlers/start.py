from aiogram.types import Message
from aiogram import F, Router
from zoneinfo import ZoneInfo
import uuid

from keyboards.inline import add_driver_with_token
from keyboards.reply import driver_menu_kb, admin_menu_kb, contact_admin_kb, pass_button
from services.request_store import save_request
from utils.auth import check_admin, check_drivers, get_admin_id

router = Router()


@router.message(F.text == '/start')
async def start(message: Message):
    """
        Реакция на команду /start.
    """

    user_id = message.from_user.id
    if check_admin(user_id):
        await message.answer("Привет, admin.", reply_markup=admin_menu_kb())

    elif check_drivers(user_id):
        await message.answer("Привет, водитель.", reply_markup=driver_menu_kb())

    else:
        await message.answer('У вас нет доступа. Свяжитесь с администратором', reply_markup=contact_admin_kb())


@router.message(F.text == '💬 Связаться с менеджером')
async def contact_admin(message: Message):
    """
        Связь с менеджером
    """

    full_name = message.from_user.full_name or 'Нет имени'
    user_name = f'@{message.from_user.username}' or 'Нет имя пользователя'
    user_id = message.from_user.id

    local_time = message.date.astimezone(ZoneInfo('Asia/Yekaterinburg'))

    admin_message = (
        f'🔔 Вам пришло уведомление\n'
        f'👤 От: {full_name}, {user_name}\n'
        f'🆔 ID: {user_id}\n'
        f'🕑 Дата и время: {local_time.strftime("%d/%m/%Y %H:%M")}\n'
    )

    token = uuid.uuid4().hex
    save_request(token, {'user_id': user_id, 'full_name': full_name, 'user_name': user_name})

    admin_id = get_admin_id()

    await message.bot.send_message(admin_id, admin_message, reply_markup=add_driver_with_token(token, user_name))
    await message.answer('📨 Ваше сообщение отправленно администратору, ожидайте обратную связь.',
                         reply_markup=pass_button())
