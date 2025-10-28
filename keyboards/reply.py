from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup, ReplyKeyboardBuilder


def get_id_kb():
    """
        Получение ID пользователя.
    """

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Получить ID")]], resize_keyboard=True
    )


def admin_menu():
    """
        Меню администратора.
    """

    pass


def driver_menu():
    """
        Меню водителя.
    """

    pass


def contact_admin_kb():
    """
        Кнопка связи с администратором.
    """

    builder = ReplyKeyboardBuilder()
    builder.button(text="💬 Связаться с менеджером")
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)