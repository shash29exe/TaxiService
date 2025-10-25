from config import ADMIN_ID, DRIVERS_ID


def check_admin(user_id: int):
    """
        Проверка на админа.
    """

    return user_id == ADMIN_ID


def check_drivers(user_id: int):
    """
        Проверка на админа.
    """

    return user_id in DRIVERS_ID
