import asyncio
from typing import Any

from gspread import Client, Worksheet, authorize
from gspread.exceptions import SpreadsheetNotFound
from gspread.utils import ValueInputOption
from oauth2client.service_account import ServiceAccountCredentials

from .config import GOOGLE_CREDENTIALS_PATH, GOOGLE_SHEET_ID, GOOGLE_SHEET_TAB_NAME
from .exceptions import GoogleClientError


class GoogleClient:
    def __init__(
        self,
        credentials_path: str = GOOGLE_CREDENTIALS_PATH,
        sheet_id: str = GOOGLE_SHEET_ID,
    ) -> None:
        self.credentials_path = credentials_path
        self.sheet_id = sheet_id
        self.sheet: dict[str, Worksheet] = {}
        self.__client: Client | None = None

    def get_worksheet_sync(self, tab_name: str = GOOGLE_SHEET_TAB_NAME) -> Worksheet:
        is_authorized = True
        if not self.__client:
            is_authorized = False
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_path,
                ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"],
            )
            self.__client = authorize(creds)
        try:
            return self.__client.open_by_key(self.sheet_id).worksheet(tab_name)
        except PermissionError as e:
            self.__client = None
            if not is_authorized:
                raise GoogleClientError("Проблема авторизации. Напишите администратору") from e
            return self.get_worksheet_sync(tab_name)
        except SpreadsheetNotFound as e:
            raise GoogleClientError(
                f"Проблема с гугл листом ({self.sheet_id} not found). Напишите администратору"
            ) from e

    async def get_worksheet(self, tab_name: str = GOOGLE_SHEET_TAB_NAME) -> Worksheet:
        if tab_name not in self.sheet:
            self.sheet[tab_name] = await asyncio.to_thread(self.get_worksheet_sync, tab_name)
        return self.sheet[tab_name]

    async def append_row(self, values: list[str], tab_name: str = GOOGLE_SHEET_TAB_NAME) -> None:
        if tab_name not in self.sheet:
            self.sheet[tab_name] = await self.get_worksheet(tab_name)
        await asyncio.to_thread(self.append_row_sync, self.sheet[tab_name], values)

    def append_row_sync(self, sheet: Worksheet, values: list[str]) -> None:
        sheet.append_row(values, value_input_option=ValueInputOption.raw)

    async def get_tab_data(self, tab_name: str = GOOGLE_SHEET_TAB_NAME) -> list[list[Any]]:
        if tab_name not in self.sheet:
            self.sheet[tab_name] = await self.get_worksheet(tab_name)
        return await asyncio.to_thread(lambda: self.sheet[tab_name].get_all_values())
