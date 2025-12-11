from config import ADMIN_ID, DRIVERS_ID
from services.google_sheets import get_drivers_from_sheets


def check_admin(user_id: int):
    """
        Проверка на админа.
    """

    return user_id == ADMIN_ID


def check_drivers(user_id: int):
    """
        Проверка id водителя на наличие в googlesheets.
    """

    allowed_users = get_drivers_from_sheets()

    return user_id in allowed_users

def get_admin_id():
    """
        Получение admin_id
    """
    return ADMIN_ID