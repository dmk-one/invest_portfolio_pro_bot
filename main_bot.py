from aiogram import Bot, Dispatcher, executor

from settings import BOT_TOKEN_API
from src.middlewares.bot import ResourceMiddleware
from src.handlers import bot as bot_handlers

bot = Bot(BOT_TOKEN_API)
dp = Dispatcher(bot)


async def on_startup(_):
    print('BOT STARTED !!!')


if __name__ == '__main__':
    dp.middleware.setup(ResourceMiddleware())

    bot_handlers.MetaHandler.register_all_handlers(dispatcher=dp)

    executor.start_polling(
        dispatcher=dp,
        on_startup=on_startup
    )
