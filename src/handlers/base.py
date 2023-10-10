from abc import ABCMeta, abstractmethod
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


class MetaHandler(ABCMeta):
    handler_cls_list = []

    def __new__(metacls, name, bases, dct):
        handler_cls = super().__new__(metacls, name, bases, dct)
        metacls.handler_cls_list.append(handler_cls)

        return handler_cls

    @staticmethod
    async def cmd_cancel(message: types.Message, state: FSMContext, *args, **kwargs):
        if state is None:
            return

        await state.finish()
        await message.reply('Вы прервали создание записи!', reply_markup=None)
                            # reply_markup=get_kb())

    @classmethod
    def register_all_handlers(cls, dispatcher: Dispatcher):
        dispatcher.register_message_handler(cls.cmd_cancel, commands=['cancel'], state='*')

        for handler_cls in cls.handler_cls_list:
            if not handler_cls.is_base():
                handler_cls().register_handlers(dispatcher=dispatcher)


class BaseHandler(metaclass=MetaHandler):
    _is_base = True

    def __init_subclass__(cls, **kwargs):
        cls._is_base = False
        super().__init_subclass__(**kwargs)

    @classmethod
    def is_base(cls):
        return cls._is_base

    @abstractmethod
    def register_handlers(self, dispatcher: Dispatcher):
        ...
