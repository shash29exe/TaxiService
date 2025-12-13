from aiogram import BaseMiddleware
import config
from keyboards.reply import contact_admin_kb
from services.google_sheets import get_drivers_from_sheets
from typing import Dict, Callable, Any, Awaitable


class CheckDriverMiddleware(BaseMiddleware):
    """
        Проверка доступа пользователя на наличие прав доступа к сервису
    """

    OPEN_COMMANDS = {
        '/start',
        '💬 Связаться с менеджером'
    }

    async def __call__(
            self,
            handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
            event,
            data: Dict[str, Any]
    ):
        user_id = None
        if hasattr(event, 'from_user'):
            user_id = event.from_user.id

        elif hasattr(event, 'message') and hasattr(event.message, 'from_user'):
            user_id = event.message.from_user.id

        if not user_id:
            return await handler(event, data)

        if user_id == config.ADMIN_ID:
            return await handler(event, data)

        text = getattr(event, 'text', None)
        if not text and hasattr(event, 'message'):
            text = event.message.text

        if text in self.OPEN_COMMANDS:
            return await handler(event, data)

        allowed_ids = get_drivers_from_sheets()
        if user_id not in allowed_ids:
            try:
                if hasattr(event, 'answer'):
                    await event.answer('У вас нет доступа. Свяжитесь с менеджером.', reply_markup=contact_admin_kb())

                elif hasattr(event, 'message') and hasattr(event.message, 'answer'):
                    await event.message.answer('У вас нет доступа.', reply_markup=contact_admin_kb())

            except:
                pass

            return

        return await handler(event, data)

