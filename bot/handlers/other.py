from aiogram import types, Router

other_router = Router(name=__name__)


@other_router.message()
async def handle_unknown(message: types.Message):
    await message.answer(
        "Отправлена неизвестная команда\nДля возвращения в меню напишете /menu"
    )
