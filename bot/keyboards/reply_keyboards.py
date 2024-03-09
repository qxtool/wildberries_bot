from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_menu_keyboard() -> ReplyKeyboardMarkup:
	keyboard = [
		[KeyboardButton(text='Получить информацию по товару')],
		[KeyboardButton(text='Остановить уведомления')],
		[KeyboardButton(text='Получить информацию из БД')],
	]
	return ReplyKeyboardMarkup(
		keyboard=keyboard,
		resize_keyboard=True,
	)


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
	keyboard = [
		[KeyboardButton(text='Отмена')],
	]
	return ReplyKeyboardMarkup(
		keyboard=keyboard,
		resize_keyboard=True
	)
