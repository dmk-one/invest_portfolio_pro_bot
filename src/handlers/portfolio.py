from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from .base import BaseHandler
from src.shared.features import set_role_validator, get_current_price
from src.controllers.portfolio import PortfolioController
from ..shared.constants import ActionType
from ..shared.keyboards import get_cancel_kb, get_is_current_data_kb, get_action_type_kb
from ..shared.states import PortfolioRecordCreationStatesGroup


class PortfolioHandler(BaseHandler):
    portfolio_controller = PortfolioController()

    start_state_text = """
        Введите тикер крипто актива (например: BTC):
    """

    is_current_data_state_text = """
        Будем использовать текущую цену актива? (Да/Нет)
        Если нет то вы дальше сами укажите дату и цену покупки/продажи актива
    """

    wrong_ticker_text = """
        Введенный крипто тикер не найден, либо вы ввели не правильный тикер, либо мы не отслеживаем этот актив
    """

    wrong_data_text = """
        Некорректные данные, создание операции отменена
    """

    enter_operation_date_text = """
        Введите дату операции в формате - день/месяц/год
    """

    @set_role_validator(allowed_role_list=['*'])
    async def get_current_price(self, message: types.Message, *args, **kwargs):
        await message.reply(text='OK')

    @set_role_validator(allowed_role_list=['*'])
    async def get_my_tickers(self, message: types.Message, *args, **kwargs):
        await self.portfolio_controller.get_user_portfolio_tickers(message['from']['id'])
        await message.reply(text='OK')




    @set_role_validator(allowed_role_list=['*'])
    async def create_portfolio_record__start_state(self, message: types.Message) -> None:
        await message.reply(self.start_state_text, reply_markup=get_cancel_kb())
        await PortfolioRecordCreationStatesGroup.crypto_ticker.set()

    async def create_portfolio_record__on_crypto_ticker_state(self, message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            data['crypto_ticker'] = message.text

        await message.reply(self.is_current_data_state_text, reply_markup=get_is_current_data_kb())
        await PortfolioRecordCreationStatesGroup.is_current_data_will_be_used.set()

    async def create_portfolio_record__on_is_current_data_state(self, message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            current_price = await get_current_price(data['crypto_ticker'])

            if not current_price:
                await state.finish()
                await message.reply(text=self.wrong_ticker_text)
                return

            is_current_data: str = message.text.lower()

            if is_current_data == 'да':
                data['by_price'] = current_price
                await message.reply("Тип операции:", reply_markup=get_action_type_kb())
                await PortfolioRecordCreationStatesGroup.action_type.set()
            elif is_current_data == 'нет':
                await message.reply(self.enter_operation_date_text, reply_markup=get_cancel_kb())
                await PortfolioRecordCreationStatesGroup.action_date.set()
            else:
                await state.finish()
                await message.reply(text=self.wrong_data_text)

    async def create_portfolio_record__on_action_date_state(self, message: types.Message, state: FSMContext) -> None:
        return

    async def create_portfolio_record__on_action_type_state(self, message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            action_type: str = message.text.lower()

            if action_type == 'покупка':
                data['action_type'] = ActionType.BUY.value
            elif action_type == 'продажа':
                data['action_type'] = ActionType.SELL.value
            else:
                await state.finish()
                await message.reply(text=self.wrong_data_text)
                return

        await message.reply("Введите количество (Целое число либо с пл.запятой):", reply_markup=get_cancel_kb())
        await PortfolioRecordCreationStatesGroup.value.set()

    async def create_portfolio_record__on_value_state(self, message: types.Message, state: FSMContext) -> None:
        async with state.proxy() as data:
            value: float = float(message.text)

            await self.portfolio_controller.create_portfolio_record(
                tg_id=message['from']['id'],
                crypto_ticker=data['crypto_ticker'],
                action_date=data['action_date'],
                action_type=data['action_type'],
                by_price=data['by_price'],
                value=value
            )

            await state.finish()
            await message.reply(text="Операция добавлена, данные портфеля обновлены!")




    def register_handlers(self, dispatcher: Dispatcher):
        dispatcher.register_message_handler(self.get_current_price, commands=['get_price'])
        dispatcher.register_message_handler(self.get_my_tickers, commands=['my_tickers'])
        dispatcher.register_message_handler(self.create_portfolio_record__start_state, commands=['create_record'])
