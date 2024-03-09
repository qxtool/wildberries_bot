import emoji
from aiogram import Bot

from bot.database.orm import ORM


async def send_subscriptions(bot: Bot):
    subscriptions = await ORM.get_all_subscribers()
    for subscription in subscriptions:
        product = subscription.product

        await bot.send_message(
            chat_id=subscription.user_id,
            text=f'Новая цена товара "{product.name}"\n'
            f"С артикулом №{product.article}\n"
            f"Равна: {product.sale_price}₽\n"
            f"Старая цена равна: {product.price}₽\n"
            f'Рейтинг товара - {product.rating}{emoji.emojize(":star:")}\n'
            f"Количество на складе: {product.count} шт.\n",
        )
