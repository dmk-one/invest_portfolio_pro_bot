from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/cancel'))

    return kb


def get_is_current_data_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Да'))
    kb.add(KeyboardButton('Нет'))
    kb.add(KeyboardButton('/cancel'))

    return kb


def get_action_type_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Покупка'))
    kb.add(KeyboardButton('Продажа'))
    kb.add(KeyboardButton('/cancel'))

    return kb
