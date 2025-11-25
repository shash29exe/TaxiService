import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
DRIVERS_ID = []
GOOGLE_CREDENTIALS_PATH=os.getenv("GOOGLE_CREDS_PATH", "services/creds/credentials.json")