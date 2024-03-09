import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.callbacks.callbacks import SubscribeCallback
from bot.database.orm import ORM
from bot.keyboards import reply_keyboards
from bot.utils.stateforms import ArticleState

callback_router = Router(name=__name__)


@callback_router.callback_query(ArticleState.get_article, SubscribeCallback.filter())
async def subscribe_callback_handler(query: CallbackQuery, state: FSMContext):
    menu_markup = reply_keyboards.get_menu_keyboard()
    data = await state.get_data()
    product = data["product"]
    await ORM.insert_subscription(
        user_id=query.from_user.id, article_id=product["article"]
    )
    logging.info(f'Product №{product["article"]} added to database')
    await query.message.delete()
    await query.message.answer(
        f'Вы подписались на обновления товара "{product["name"]}"'
        f' с артикулом №{product["article"]}',
        reply_markup=menu_markup,
    )
    await state.clear()


@callback_router.callback_query(SubscribeCallback.filter())
async def subscribe_callback_handler(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer(
        f"Ошибка при подписке\n" f"Данные о товаре могли обновится",
    )
