from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton


def user_start_kbd() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Заказать лабу"),
               KeyboardButton("Помощь"),
               KeyboardButton("Mои заказы"))

    return markup


def worker_start_kbd() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Получить список заказов"),
               KeyboardButton("Помощь"),
               KeyboardButton("Mои работы"))

    return markup


def languages_kbd() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("C++"),
               KeyboardButton("Java"),
               KeyboardButton("ASSEMBLER"))

    return markup


def empty_description_kbd() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Дополнительных сведений нет"))

    return markup


def clear_kbd() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardRemove()

    return markup


def accept_order_ikb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Принять", callback_data='accept_order')],
        [InlineKeyboardButton("Отклонить", callback_data='decline_order')],
        [InlineKeyboardButton("Заблокировать пользователя", callback_data='ban_user')]
    ])

    return markup


def worker_watch_ikb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Предложить цену", callback_data='offer_price')]
        # TODO exclametion
    ])

    return markup


def user_accept_price_ikb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Принять цену", callback_data='accept_price')]
        # TODO exclametion
    ])

    return markup
