from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.inline import pay_button
from utils.payments import create_payment

router = Router()


@router.message(Command('pay'))
async def pay(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name
    amount = 500.00
    description = f'Пополнение баланса от {username}({user_id}).'

    try:
        confirmation_url, payment_id = await create_payment(amount, description, user_id, username)

    except Exception as e:
        await message.answer(f'Ошибка платежа: {e}.')
        return

    kb = pay_button(amount, confirmation_url)
    await message.answer(f'Счёт создан. ID Платежа: {payment_id}.\nДля оплаты нажмите на кнопку 👇', reply_markup=kb, parse_mode='Markdown')
