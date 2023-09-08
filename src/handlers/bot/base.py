from abc import ABCMeta, abstractmethod
from aiogram import Dispatcher


class MetaHandler(ABCMeta):
    handler_cls_list = []

    def __new__(metacls, name, bases, dct):
        handler_cls = super().__new__(metacls, name, bases, dct)
        metacls.handler_cls_list.append(handler_cls)

        return handler_cls

    @classmethod
    def register_all_handlers(cls, dispatcher: Dispatcher):
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
