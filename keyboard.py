from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton


def user_start_ikb() -> ReplyKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Заказать лабу", callback_data='create_order')],
        [InlineKeyboardButton("Помощь", callback_data='help')],
        [InlineKeyboardButton("Мои заказы", callback_data='user_orders')]
    ])
    return markup


def worker_start_ikb() -> ReplyKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Список заказов", callback_data='free_orders')],
        [InlineKeyboardButton("Помощь", callback_data='help')],
        [InlineKeyboardButton("Мои работы", callback_data='worker_orders')]
    ])

    return markup


def help_ikb() -> ReplyKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Как создать заказ?", callback_data='how_to_create_order')],
        [InlineKeyboardButton("Как оплатить заказ?", callback_data='how_to_pay_order')],
        [InlineKeyboardButton("Обратиться в поддержку", callback_data='contact_support')]
    ])

    return markup


def how_to_pay_ikb() -> ReplyKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Как оплатить заказ?", callback_data='how_to_pay_order1')]
    ])

    return markup


def languages_kbd() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("C++"),
               KeyboardButton("Java"),
               KeyboardButton("ASSEMBLER"))

    return markup


def bool_kbd() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Да"),
               KeyboardButton("Нет"))

    return markup


def empty_description_kbd() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Дополнительных сведений нет"))

    return markup


def clear_kbd() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardRemove()

    return markup


def clear_ikb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()

    return markup


def accept_order_ikb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Принять", callback_data='accept_order')],
        [InlineKeyboardButton("Отклонить", callback_data='decline_order')]
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
        [InlineKeyboardButton("Отправить жалобу", callback_data='send_exclamation')]
    ])

    return markup


def worker_work_ikb() ->InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Отправить жалобу", callback_data='send_exclamation')],
        [InlineKeyboardButton("Заказ выполнен", callback_data='order_executed')]
    ])

    return markup


def user_accept_solution_ikb() ->InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Подтвердить выполнение заказа", callback_data='accept_solution')],
        [InlineKeyboardButton("Отправить жалобу", callback_data='send_exclamation')]
    ])

    return markup


def exclamation_ikb() ->InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Прав заказчик", callback_data='user_r')],
        [InlineKeyboardButton("Прав работник", callback_data='worker_r')],
        [InlineKeyboardButton("Отклонить спор", callback_data='decline_excl')]
    ])

    return markup


def worker_taken_orders_ikb() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Взятые работы", callback_data='worker_orders')]
    ])

    return markup