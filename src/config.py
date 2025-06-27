import os

from dotenv import load_dotenv

load_dotenv()

GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "Questionnaire")
GOOGLE_SHEET_TAB_NAME = os.getenv("GOOGLE_SHEET_TAB_NAME", "Sheet1")

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "")
ADMIN_IDS = os.getenv("ADMIN_IDS", "0").split(",")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
