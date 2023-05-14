from aiogram import Dispatcher, types

from .base import BaseHandler
from src.shared.features import set_role_validator


class OtherHandler(BaseHandler):
    async def helper(self, message: types.Message, *args, **kwargs):
        await message.reply(text='/111 - test \n /222 - test')

    @set_role_validator(allowed_role_list=['*'])
    async def starter(self, message: types.Message, *args, **kwargs):
        await message.answer(text='HI')
        await message.delete()

    def register_handlers(self, dispatcher: Dispatcher):
        dispatcher.register_message_handler(self.helper, commands=['help'])
        dispatcher.register_message_handler(self.starter, commands=['start', 'restart'])
