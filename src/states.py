from aiogram.fsm.state import State, StatesGroup


class FeedbackForm(StatesGroup):
    waiting_for_id = State()
    waiting_for_feedback = State()
