import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
DRIVERS_ID = [7003041125, 1721435667]
GOOGLE_CREDENTIALS_PATH=os.getenv("GOOGLE_CREDENTIAL_PATH", "services/creds/credentials.json")