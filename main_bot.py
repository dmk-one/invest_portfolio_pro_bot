from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from settings import BOT_TOKEN_API
from src.middlewares import ResourceMiddleware
from src.handlers.base import MetaHandler

storage = MemoryStorage()
bot = Bot(BOT_TOKEN_API)
dp = Dispatcher(bot, storage)


async def on_startup(_):
    print('BOT STARTED !!!')


def init_all_handlers():
    from src.handlers.other import ExtraHandler
    from src.handlers.portfolio import PortfolioHandler


if __name__ == '__main__':
    dp.middleware.setup(ResourceMiddleware())

    init_all_handlers()

    MetaHandler.register_all_handlers(dispatcher=dp)

    executor.start_polling(
        dispatcher=dp,
        on_startup=on_startup
    )
