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
    ])

    return markup


def user_accept_price_ikb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Принять цену", callback_data='accept_price')]
        # TODO exclametion
    ])

    return markup


def user_work_02_ikb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Удалить заказ", callback_data='delete_order')]
    ])

    return markup


def user_work_1_ikb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Проверить предложения", callback_data='check_offers')],
        [InlineKeyboardButton("Удалить заказ", callback_data='delete_order')]
    ])

    return markup

def user_work_3_ikb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Отправить жалобу", callback_data='send_exclamation')],
        [InlineKeyboardButton("Проверить дедлайн", callback_data='check_deadline')],
        [InlineKeyboardButton("Заказ выполнен!", callback_data='accept_solution')]
        # TODO exclametion
    ])

    return markup


def worker_work_ikb() ->InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Отправить жалобу", callback_data='send_exclamation')]

    ])

    return markup