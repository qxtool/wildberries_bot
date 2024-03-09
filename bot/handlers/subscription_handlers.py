from aiogram import types, Router, F

from bot.database.orm import ORM
from bot.keyboards import reply_keyboards

subscription_router = Router(name=__name__)


@subscription_router.message(F.text == "Остановить уведомления")
async def get_article(message: types.Message):
    menu_markup = reply_keyboards.get_menu_keyboard()
    await ORM.delete_subscriptions_for_user(user_id=message.from_user.id)
    await message.answer("Вы отписались от всех уведомлений", reply_markup=menu_markup)
