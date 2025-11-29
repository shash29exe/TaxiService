PENDING_REQUESTS: dict = {}


def save_request(token: str, data: dict):
    """
        Сохранение запроса
    """

    PENDING_REQUESTS[token] = data


def get_request(token: str):
    """
        Получение запроса
    """

    return PENDING_REQUESTS.get(token)


def remove_requests(token: str):
    """
        Удаление запроса
    """

    PENDING_REQUESTS.pop(token, None)
