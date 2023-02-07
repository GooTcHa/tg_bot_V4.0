from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton


def get_user_start_kbd() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Заказать лабу"),
               KeyboardButton("Помощь"),
               KeyboardButton("Mои заказы"))

    return markup


def get_worker_start_kbd() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Получить список заказов"),
               KeyboardButton("Помощь"),
               KeyboardButton("Mои работы"))

    return markup


def get_languages_kbd() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("C++"),
               KeyboardButton("Java"),
               KeyboardButton("ASSEMBLER"))

    return markup


def get_empty_description_kbd() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Дополнительных сведений нет"))

    return markup


def clear_kbd() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardRemove()

    return markup
