from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup, ReplyKeyboardBuilder


def pass_button():
    """
        Удаление кнопки
    """

    builder = ReplyKeyboardBuilder()
    builder.button(text='Дождитесь соединения с сервисом.')
    return builder.as_markup(resize_keyboard=True)


def admin_menu_kb():
    """
        Меню администратора.
    """

    builder = ReplyKeyboardBuilder()
    builder.button(text='Сводный отчёт')
    builder.button(text='Выгрузка')
    builder.button(text='Удалить водителя')
    builder.adjust(2, 1)

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
        Меню доходов.
    """

    builder = ReplyKeyboardBuilder()
    builder.button(text="Оплата за заказ")
    builder.button(text="Доплата за заказ")
    builder.button(text="🔙 Назад")
    builder.adjust(2, 1)

    return builder.as_markup(resize_keyboard=True)


def back_button_kb():
    """
        Кнопка шаг назад.
    """

    builder = ReplyKeyboardBuilder()
    builder.button(text="Назад 🔙")

    return builder.as_markup(resize_keyboard=True)


def back_to_driver_kb():
    """
        Кнопка назад в меню водителя.
    """

    builder = ReplyKeyboardBuilder()
    builder.button(text='🔙 Назад в меню')

    return builder.as_markup(resize_keyboard=True)


def driver_report_select_date():
    """
        Выбор определённого периода для отчёта водителя.
    """

    builder = ReplyKeyboardBuilder()
    builder.button(text="Текущий день")
    builder.button(text="За месяц")
    builder.button(text="🔙 Назад")
    builder.adjust(2, 1)

    return builder.as_markup(resize_keyboard=True)


def admin_summary_kb():
    """
        Выбор периода для отчёта.
    """

    builder = ReplyKeyboardBuilder()
    builder.button(text="Сегодня")
    builder.button(text="Этот месяц")
    builder.button(text="Всё время")
    builder.button(text="↩️ Назад")
    builder.adjust(3, 1)

    return builder.as_markup(resize_keyboard=True)


def admin_export_kb():
    """
        Выгрузка данных за определённый период
    """

    builder = ReplyKeyboardBuilder()
    builder.button(text="📆 За день")
    builder.button(text="📆 За месяц")
    builder.button(text="📆 За всё время")
    builder.button(text="↩️ Назад")
    builder.adjust(3, 1)
    return builder.as_markup(resize_keyboard=True)
