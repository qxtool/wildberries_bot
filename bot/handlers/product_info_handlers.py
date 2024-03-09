import logging

import emoji
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager, StartMode

from bot.keyboards import reply_keyboards, inline_keyboards
from bot.utils.stateforms import ArticleState, ProductsDialogState
from bot.utils.wildberries import fetch_product

product_router = Router(name=__name__)


@product_router.message(ArticleState.get_article, F.text.isdigit())
async def get_article(message: types.Message, state: FSMContext):
    cancel_markup = reply_keyboards.get_cancel_keyboard()
    try:
        subscribe_markup = inline_keyboards.get_subscribe_keyboard()
        product = await fetch_product(message.text)
        await message.answer(
            f'Новая цена товара "{product.name}"\n'
            f"С артикулом №{product.article}\n"
            f"Равна: {product.sale_price}₽\n"
            f"Старая цена равна: {product.price}₽\n"
            f'Рейтинг товара - {product.rating}{emoji.emojize(":star:")}\n'
            f"Количество на складе: {product.count} шт.\n",
            reply_markup=cancel_markup,
        )
        await message.answer(
            "Также вы можете подписаться на уведомления", reply_markup=subscribe_markup
        )
        product = dict(product)
        product["price"] = product.pop("price_raw") // 100
        product["sale_price"] = product.pop("sale_price_raw") // 100
        await state.set_data({"product": product})  # For subscribe_markup callback
    except Exception as e:
        logging.error(e)
        await message.answer(
            "Не удалось получить данные\n" "Проверьте артикул",
            reply_markup=cancel_markup,
        )


@product_router.message(ArticleState.get_article)
async def get_wrong_article(message: types.Message):
    await message.answer(
        "Отправьте корректный артикул", reply_markup=message.reply_markup
    )


@product_router.message(F.text == "Получить информацию по товару")
async def get_info(message: types.Message, state: FSMContext):
    cancel_markup = reply_keyboards.get_cancel_keyboard()
    await state.set_state(ArticleState.get_article)
    await message.answer("Отправьте артикул товара", reply_markup=cancel_markup)


@product_router.message(F.text == "Получить информацию из БД")
async def get_last_5_products(message: types.Message, dialog_manager: DialogManager):
    menu_markup = reply_keyboards.get_menu_keyboard()
    await dialog_manager.start(ProductsDialogState.LIST, mode=StartMode.RESET_STACK)
    await message.answer(
        text="Вы получили последние записи о товарах", reply_markup=menu_markup
    )


# @product_router.message(F.text == "Получить информацию из БД")
# async def get_last_5_products(message: types.Message):
#     menu_markup = reply_keyboards.get_menu_keyboard()
#     last_5_products = list(await ORM.get_last_5_products())
#     if not last_5_products:
#         await message.answer("Не удалось получить последние 5 записей из базы данных")
#     for product in reversed(
#         last_5_products
#     ):
#         product = product[0]
#         await message.answer(
#             f'Новая цена товара "{product.name}"\n'
#             f"С артикулом №{product.article}\n"
#             f"Равна: {product.sale_price}₽\n"
#             f"Старая цена равна: {product.price}₽\n"
#             f'Рейтинг товара - {product.rating}{emoji.emojize(":star:")}\n'
#             f"Количество на складе: {product.count} шт.\n",
#         )
#     if last_5_products:
#         await message.answer(
#             f"Вы получили последние {len(last_5_products)} записей из базы данных",
#             reply_markup=menu_markup,
#         )
