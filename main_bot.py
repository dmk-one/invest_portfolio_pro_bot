from aiogram import Bot, Dispatcher, executor, types

from settings import BOT_TOKEN_API
from src.middlewares.bot import ResourceMiddleware

bot = Bot(BOT_TOKEN_API)
dp = Dispatcher(bot)


@dp.message_handler(commands=['help'])
async def helper(message: types.Message, async_session=None, **kwargs):
    from single_session import single_session

    print('single_session in main', single_session, id(single_session))

    # print('async_session', async_session)
    #
    # for key, val in kwargs.items():
    #     print('\nKWARGS KEY', key)
    #     print('\nKWARGS VAL', val)
    #
    # from src.models import Portfolio
    #
    # n_p = Portfolio(
    #     tg_id=12345,
    #     crypto='asfsafesafgs'
    # )
    #
    # async_session.add(n_p)
    #
    # await message.reply(text='/111 - test \n /222 - test')


@dp.message_handler(commands=['start'])
async def starter(message: types.Message):
    await message.answer(text='HI')
    await message.delete()


async def on_startup(_):
    print('BOT STARTED !!!')


if __name__ == '__main__':
    dp.middleware.setup(ResourceMiddleware())
    executor.start_polling(
        dispatcher=dp,
        on_startup=on_startup
    )
