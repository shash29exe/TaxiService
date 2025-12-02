from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def add_driver_with_token(token: str, driver_name: str):
   """
        Кнопка добавления водителя.
   """

   callback_data = f'add_driver:{token}'

   return InlineKeyboardMarkup(
       inline_keyboard=[
           [InlineKeyboardButton(
               text=f'Добавить водителя {driver_name}', callback_data=callback_data),
           ]
       ]
   )


def pay_button(amount:float, url:str):
    """
        Кнопка для оплаты
    """

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f'Оплатить ({amount:.0f}₽)',
                url=url
            )]
        ]
    )