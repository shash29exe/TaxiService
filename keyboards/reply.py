from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup


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


def contact_admin():
    """
        Кнопка связи с администратором.
    """

    pass