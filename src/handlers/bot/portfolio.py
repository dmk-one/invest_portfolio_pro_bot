from aiogram import Dispatcher, types

from .base import BaseHandler
from src.shared.features import set_role_validator


class PortfolioHandler(BaseHandler):
    starter_text = """
    Добро пожаловать в простой бот для отслеживания крипто портфеля
    """

    @set_role_validator(allowed_role_list=['*'])
    async def get_current_price(self, message: types.Message, *args, **kwargs):
        await message.reply(text=self.helper_text)

    @set_role_validator(allowed_role_list=['*'])
    async def starter(self, message: types.Message, *args, **kwargs):
        await message.answer(text=self.starter_text)
        await message.delete()

    def register_handlers(self, dispatcher: Dispatcher):
        dispatcher.register_message_handler(self.helper, commands=['help'])
        dispatcher.register_message_handler(self.starter, commands=['start', 'restart'])