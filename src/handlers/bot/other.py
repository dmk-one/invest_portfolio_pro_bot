from aiogram import Dispatcher, types
from .base import BaseHandler


class OtherHandler(BaseHandler):
    async def helper(self, message: types.Message, *args, **kwargs):
        await message.reply(text='/111 - test \n /222 - test')

    async def starter(self, message: types.Message, *args, **kwargs):
        await message.answer(text='HI')
        await message.delete()

    def register_handlers(self, dispatcher: Dispatcher):
        dispatcher.register_message_handler(self.helper, commands=['help'])
        dispatcher.register_message_handler(self.starter, commands=['start', 'restart'])
