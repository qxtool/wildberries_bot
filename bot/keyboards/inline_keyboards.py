from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.callbacks import callbacks


def get_subscribe_keyboard() -> InlineKeyboardMarkup:
    callback_data = callbacks.SubscribeCallback().pack()
    keyboard = [
        [InlineKeyboardButton(text="Подписаться", callback_data=callback_data)],
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=keyboard,
    )
