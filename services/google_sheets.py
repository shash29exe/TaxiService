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

def add_record(record_type:str, subcategory:str, amount:float, comment:str, user_id:int, username:str):
    """
        Добавление записи google sheets.
    """

    now = datetime.now()
    row = [
        now.strftime("%d/%m/%Y"),
        now.strftime("%H:%M:%S"),
        record_type,
        subcategory,
        amount,
        comment,
        user_id,
        username
    ]

    sheet.append_row(row, value_input_option='USER_ENTERED')


def get_records_by_day(telegram_id, today):
    pass