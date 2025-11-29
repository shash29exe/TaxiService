from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.reply import driver_menu_kb
from services.google_sheets import add_record
from services.request_store import get_request, remove_requests

router = Router()


@router.callback_query(F.data.startswith("add_driver:"))
async def add_driver_callback(callback: CallbackQuery):
    """
        Добавление водителя через инлайн кнопку
    """

    _, token = callback.data.split(':', 1)

    data = get_request(token)
    if not data:
        await callback.answer('Данные отсутствуют.', show_alert=True)
        return

    driver_id = data['user_id']
    driver_name = data['user_name']

    add_record(
        user_id=driver_id,
        username=driver_name,
        record_type='водитель',
        subcategory='добавление',
        amount=0,
        comment='новый водитель добавлен'
    )

    remove_requests(token)

    new_text = callback.message.text + '\nВодитель зарегестрирован'
    await callback.message.edit_text(new_text)
    await callback.answer('Готово')

    try:
        await callback.bot.send_message(driver_id, 'Добро пожаловать!', reply_markup=driver_menu_kb())

    except:
        pass