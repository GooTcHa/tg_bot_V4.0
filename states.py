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
    user_set_price = State()
    successful_user_payment_state = State()
    user_enter_reject_state = State()

    """ADMIN STATES"""
    admin_decline_order_state = State()

    """GENERAL STATES"""
    exclamation_state = State()
    pre_exclamation_state = State()
    send_exclamation_state = State()
