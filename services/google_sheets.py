import json
from datetime import datetime
# import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from config import GOOGLE_CREDENTIALS_PATH

# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# credential_path = os.path.join(base_dir, 'services', 'creds', 'credentials.json')

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
