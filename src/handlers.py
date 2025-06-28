from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from google_lib.google_sheets_client import GoogleSheetsClient

from .cache import ConferenceCache
from .config import ADMIN_IDS, GOOGLE_CREDENTIALS_PATH, GOOGLE_SHEET_ID
from .states import FeedbackForm

router = Router()


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(router)


@router.message(Command("start"))
async def cmd_start(msg: Message, state: FSMContext) -> None:
    await msg.answer("Введите ID конференции:")
    await state.set_state(FeedbackForm.waiting_for_id)


@router.message(FeedbackForm.waiting_for_id)
async def cmd_receive_id(msg: Message, state: FSMContext) -> None:
    conf_id = msg.text.strip()
    if conf_id not in ConferenceCache.get_config():
        await msg.answer("Конференция не найдена или недоступна.")
        return
    await state.update_data(conf_id=conf_id)
    await state.set_state(FeedbackForm.waiting_for_feedback)
    await msg.answer("Напишите ваш отзыв:")


@router.message(FeedbackForm.waiting_for_feedback)
async def cmd_receive_feedback(msg: Message, state: FSMContext) -> None:
    data = await state.get_data()
    conf_id = data["conf_id"]
    feedback = msg.text.strip()

    await GoogleSheetsClient(GOOGLE_CREDENTIALS_PATH, GOOGLE_SHEET_ID).append_row(
        [msg.from_user.full_name, msg.from_user.id, feedback], conf_id
    )
    await msg.answer("Спасибо за отзыв!")
    await state.clear()


@router.message(Command("refresh_config"))
async def cmd_refresh_config(msg: Message) -> None:
    if msg.from_user.id not in ADMIN_IDS:
        await msg.answer("Нет доступа.")
        return
    await ConferenceCache.refresh_config()
    await msg.answer("Конфиг обновлён.")
