import emoji
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import NumberedPager
from aiogram_dialog.widgets.text import Const, Format, List

from bot.database.orm import ORM
from bot.utils.stateforms import ProductsDialogState

dialog = Dialog(
    Window(
        Const("Список полученных товаров:\n"),
        List(
            Format(
                'Новая цена товара "{item.name}"\n'
                "С артикулом №{item.article}\n"
                "Равна: {item.sale_price}₽\n"
                "Старая цена равна: {item.price}₽\n"
                "Рейтинг товара - {item.rating}" + f'{emoji.emojize(":star:")}\n'
                "Количество на складе: {item.count} шт.\n",
            ),
            items="products",
            id="list_scroll",
            page_size=1,
        ),
        NumberedPager(
            scroll="list_scroll",
        ),
        getter=ORM.get_last_5_products,
        state=ProductsDialogState.LIST,
    ),
)
