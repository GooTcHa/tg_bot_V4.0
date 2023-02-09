from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    """WORKER STATES"""
    worker_start_state = State()
    worker_price_state = State()

    """USER STATES"""
    user_start_state = State()
    user_choose_language_state = State()
    user_send_photo_state = State()
    user_send_description_state = State()
