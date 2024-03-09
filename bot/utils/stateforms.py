from aiogram.fsm.state import StatesGroup, State


class ArticleState(StatesGroup):
    get_article = State()


class ProductsDialogState(StatesGroup):
    LIST = State()
