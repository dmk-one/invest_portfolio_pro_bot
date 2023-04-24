from aiogram import Bot, Dispatcher, executor, types

from settings import BOT_TOKEN_API

bot = Bot(BOT_TOKEN_API)
dp = Dispatcher(bot)


@dp.message_handler(commands=['help'])
async def helper(message: types.Message):
    await message.reply(text='/111 - test \n /222 - test')


@dp.message_handler(commands=['start'])
async def starter(message: types.Message):
    await message.answer(text='HI')
    await message.delete()

if __name__ == '__main__':
    executor.start_polling(dp)
