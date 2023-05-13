from abc import abstractmethod
from aiogram import Dispatcher
from .meta import MetaHandler


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
