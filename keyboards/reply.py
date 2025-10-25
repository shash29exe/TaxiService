from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup

def get_id():
    """
        Получение ID пользователя.
    """

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Получить ID")]], resize_keyboard=True
    )