import logging

from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from bot.database.orm import ORM
from bot.keyboards import reply_keyboards

menu_router = Router(name=__name__)


@menu_router.message(F.text == "Отмена")
async def cancel(message: types.Message, state: FSMContext):
    menu_markup = reply_keyboards.get_menu_keyboard()
    await state.clear()
    await message.answer("Вы вернулись в меню", reply_markup=menu_markup)


@menu_router.message(CommandStart())
async def handle_start(message: types.Message):
    menu_markup = reply_keyboards.get_menu_keyboard()
    user_id, name = message.from_user.id, message.from_user.full_name
    await ORM.insert_user(user_id, name)  # Good practice - middleware + redis
    logging.info(f"User {user_id} with name {name} added to database")
    await message.answer("Выберите действие: ", reply_markup=menu_markup)


@menu_router.message(Command("menu"))
async def handle_menu(message: types.Message, state: FSMContext):
    menu_markup = reply_keyboards.get_menu_keyboard()
    await state.clear()
    await message.answer("Вы вернулись в меню", reply_markup=menu_markup)
