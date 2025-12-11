import json
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import config
from config import GOOGLE_CREDENTIALS_PATH

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

with open(GOOGLE_CREDENTIALS_PATH, 'r') as f:
    creds_dict = json.load(f)

credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

files = client.list_spreadsheet_files()
for file in files:
    print(file['name'], file['id'])

SPREADSHEET_NAME = "TaxiService"

spreadsheet = client.open(SPREADSHEET_NAME)
sheet = spreadsheet.sheet1


def add_record(record_type: str, subcategory: str, amount: float, comment: str, user_id: int, username: str):
    """
        Добавление записи google sheets.
    """

    now = datetime.now()
    row = [
        now.strftime("%d.%m.%Y"),
        now.strftime("%H:%M:%S"),
        record_type,
        subcategory,
        amount,
        comment,
        user_id,
        username
    ]

    sheet.append_row(row, value_input_option='USER_ENTERED')
    update_drivers_in_config()


def get_records_by_day(user_id: int, date: str):
    """
        Получение отчёта за день.
    """

    rows = sheet.get_all_values()[1:]
    filtered_rows = []

    for row in rows:
        row_date = row[0]
        row_user_id = row[6]
        if row_date == date and str(user_id) == row_user_id:
            filtered_rows.append(row)

    return filtered_rows


def get_records_by_month(user_id: int, month: int, year: int):
    """
        Получение отчёта за месяц.
    """

    rows = sheet.get_all_values()[1:]
    filtered_rows = []

    for row in rows:
        row_date = datetime.strptime(row[0], '%d.%m.%Y')
        row_user_id = row[6]
        if row_date.month == month and row_date.year == year and str(user_id) == row_user_id:
            filtered_rows.append(row)

    return filtered_rows


def get_admin_summary(period: str):
    """
        Возможность получить отчёты по всем пользователям за все периоды
    """

    records = sheet.get_all_values()
    header = records[0]
    rows = records[1:]

    today_str = datetime.now().strftime('%d.%m.%Y')
    month_str = datetime.now().strftime('%m.%Y')

    summary = {}

    for row in rows:
        if len(row) < 8:
            continue

        date, _, record_type, _, amount, _, user_id, username = row

        if period == 'day' and date != today_str:
            continue

        if period == 'month' and not date.endswith(month_str):
            continue

        try:
            amount = float(amount.replace(',', '.'))

        except ValueError:
            continue

        if username not in summary:
            summary[username] = {'income': 0, 'expense': 0}

        if record_type.lower() == 'доход':
            summary[username]['income'] += amount

        if record_type.lower() == 'расход':
            summary[username]['expense'] += amount

    lines = []
    total_income = 0
    total_expense = 0

    for user, data in summary.items():
        lines.append(f'{user}: Доход: {data['income']:.2f}₽; Расход: {data["expense"]:.2f}₽')

        total_income += data['income']
        total_expense += data['expense']

    lines.append(
        f'\nОбщий итог:\nДоход: {total_income}₽\nРасход: {total_expense}₽\n\nПрибыль: {total_income - total_expense:.2f}₽')

    return '\n'.join(lines) if lines else 'Нет данных за выбранный период'


def get_all_data():
    """
        Получение всех данных из таблицы
    """

    return sheet.get_all_values()


def update_drivers_in_config():
    """
        Актуализация списка водителей.
    """

    try:
        current_drivers = get_drivers_from_sheets()
        if not isinstance(config.DRIVERS_ID, list):
            config.DRIVERS_ID = []

        merged = set(config.DRIVERS_ID) | set(current_drivers)
        config.DRIVERS_ID[:] = sorted(list(merged))

        print(f'Список водителей обновлён.\n{config.DRIVERS_ID}')

        return config.DRIVERS_ID

    except Exception as e:
        print(f'Ошибка при обновлении водителей:\n{e}')

        return []


def get_drivers_from_sheets():
    """
        Получение ID водителей
    """

    try:
        all_data = sheet.get_all_values()
        if len(all_data) <= 1:
            return []

        drivers_ids = set()
        for row in all_data[1:]:
            try:
                if len(row) > 6 and row[6].strip():
                    drivers_ids.add(int(row[6].strip()))
            except IndexError:
                continue

        return sorted(list(drivers_ids))

    except Exception as e:
        print(f'Ошибка при получении списка водителей:\n{e}')
        return []


def remove_driver_from_sheet(driver_id):
    try:
        all_data = sheet.get_all_values()
        if len(all_data) <= 1:
            return False

        rows_to_delete = []

        for i, row in enumerate(all_data[1:], start=2):
            try:
                if len(row) > 6 and int(row[6]) == driver_id:
                    rows_to_delete.append(i)

            except (IndexError, ValueError):
                continue

        if not rows_to_delete:
            print(f'User ID {driver_id} not found')
            return False

        for row_index in reversed(rows_to_delete):
            sheet.delete_rows(row_index)

        print(f'User deleted {driver_id}, {rows_to_delete}')
        update_drivers_in_config()
        return True

    except Exception as e:
        print('Ошибка при удалении')
        return False
