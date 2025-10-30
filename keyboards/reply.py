from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup, ReplyKeyboardBuilder


def get_id_kb():
    """
        Получение ID пользователя.
    """

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Получить ID")]], resize_keyboard=True
    )


def admin_menu_kb():
    """
        Меню администратора.
    """

    builder = ReplyKeyboardBuilder()
    builder.button(text='Сводный отчёт')
    builder.button(text='Выгрузка')
    builder.button(text='Добавить водителя')
    builder.button(text='Удалить водителя')
    builder.adjust(2, 2)

    return builder.as_markup(resize_keyboard=True)


def driver_menu_kb():
    """
        Меню водителя.
    """

    builder = ReplyKeyboardBuilder()
    builder.button(text='Доход')
    builder.button(text='Расход')
    builder.button(text='Отчёт')
    builder.adjust(1, 1, 1)

    return builder.as_markup(resize_keyboard=True)


def contact_admin_kb():
    """
        Кнопка связи с администратором.
    """

    builder = ReplyKeyboardBuilder()
    builder.button(text="💬 Связаться с менеджером")
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


def income_menu_kb():
    """
        Меню доходов
    """

    builder = ReplyKeyboardBuilder()
    builder.button(text="Оплата за заказ")
    builder.button(text="Доплата за заказ")
    builder.button(text="🔙 Назад")
    builder.adjust(2, 1)

    return builder.as_markup(resize_keyboard=True)


def back_button_kb():
    """
        Кнопка шаг назад
    """

    builder = ReplyKeyboardBuilder()
    builder.button(text="Назад 🔙")

    return builder.as_markup(resize_keyboard=True)