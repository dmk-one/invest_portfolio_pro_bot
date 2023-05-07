from aiogram import Dispatcher


class UserHandler:
    def __init__(self, dispatcher: Dispatcher):
        dispatcher.register_message_handler(self.start_bot, commands=['start', 'restart'])

    def start_bot(self):

