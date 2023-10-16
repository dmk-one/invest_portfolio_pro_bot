from datetime import datetime
from typing import List

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from .base import BaseHandler
from src.shared.features import set_role_validator, get_current_price
from src.controllers.portfolio import PortfolioController
from ..shared.constants import ActionType
from ..shared.keyboards import get_cancel_kb, get_is_current_data_kb, get_action_type_kb
from ..shared.schemas import TotalStats, TickerStat
from ..shared.states import PortfolioRecordCreationStatesGroup


class BasePortfolioHandler:
    portfolio_controller = PortfolioController()


class AdditionalPortfolioHandler(BaseHandler, BasePortfolioHandler):
    @set_role_validator(allowed_role_list=['*'])
    async def get_current_price(self, message: types.Message, *args, **kwargs):
        await message.reply(text='OK')

    @set_role_validator(allowed_role_list=['*'])
    async def get_my_tickers(self, message: types.Message, *args, **kwargs):
        await self.portfolio_controller.get_user_portfolio_tickers(message['from']['id'])
        await message.reply(text='OK')

    def register_handlers(self, dispatcher: Dispatcher):
        dispatcher.register_message_handler(self.get_current_price, commands=['get_price'])
        dispatcher.register_message_handler(self.get_my_tickers, commands=['my_tickers'])


class PortfolioStatHandler(BaseHandler, BasePortfolioHandler):
    @staticmethod
    def generate_total_stats_text(total_stats: TotalStats):
        total_stats_text = (
            "Общая статистика по портфелю:\n"
            f"Общая сумма инвестирования: {total_stats.total_invested_usd_sum}$\n"
            f"Общая сумма с текущими ценами: {total_stats.total_current_usd_sum}$\n"
            f"Сумма PNL: {total_stats.pnl_value}$\n"
            f"PNL: {total_stats.pnl_percent}%\n"
            f"Количество криптовалют: {len(total_stats.tickers_stats)}\n"
        )

        return total_stats_text

    @staticmethod
    def generate_ticker_stats_text(ticker_stats: List[TickerStat]):
        ticker_stats_text = ""

        for ticker_stat in ticker_stats:
            ticker_stats_text += (
                f"Криптовалюта: {ticker_stat.crypto}\n"
                f"Количество: {ticker_stat.total_value}\n"
                f"Средняя цена: {ticker_stat.average_price}$\n"
                f"Текущая цена: {ticker_stat.current_price}$\n"
                f"Сумма инвестирования: {ticker_stat.total_invested_usd_sum}$\n"
                f"Сумма с текущими ценами: {ticker_stat.total_current_usd_sum}$\n"
                f"Сумма PNL: {ticker_stat.pnl_value}$\n"
                f"PNL: {ticker_stat.pnl_percent}%\n\n"
            )

        return ticker_stats_text.strip()

    async def get_my_portfolio_stats(self, message: types.Message, *args, **kwargs):
        portfolio_stats = await self.portfolio_controller.get_total_portfolio_stats(message['from']['id'])
        total_stats_text = self.generate_total_stats_text(portfolio_stats)
        ticker_stats_text = self.generate_ticker_stats_text(portfolio_stats.tickers_stats)
        await message.answer(text=total_stats_text)
        await message.answer(text=ticker_stats_text)

    def register_handlers(self, dispatcher: Dispatcher):
        dispatcher.register_message_handler(self.get_my_portfolio_stats, commands=['stats'])


class CreatePortfolioRecordHandler(BaseHandler, BasePortfolioHandler):
    start_state_text = """
        Введите тикер крипто актива (например: bitcoin, polkadot):
    """

    is_current_data_state_text = """
        Будем использовать текущую цену актива? (Да/Нет)\nЕсли нет то вы дальше сами укажите дату и цену покупки/продажи актива
    """

    wrong_ticker_text = """
        Введенный крипто тикер не найден в coingecko, либо вы ввели не правильный тикер
    """

    wrong_date_text = """
        Введенная дата некорректна! Создание операции отменена
    """

    wrong_data_text = """
        Некорректные данные, создание операции отменена
    """

    wrong_price_or_value_text = """
        Некорректное значение, значение должно быть целым числом либо числом с пл.запятой
    """

    enter_operation_date_text = """
        Введите дату операции в формате - день/месяц/год
    """

    enter_price_text = """
        Введите цену актива в момент покупки (целое число либо с пл.запятой):
    """

    @set_role_validator(allowed_role_list=['*'])
    async def create_portfolio_record__start_state(
        self, message:
        types.Message,
        *args,
        **kwargs
    ) -> None:
        await message.reply(self.start_state_text, reply_markup=get_cancel_kb())
        await PortfolioRecordCreationStatesGroup.crypto_ticker.set()

    async def create_portfolio_record__on_crypto_ticker_state(
        self,
        message: types.Message,
        state: FSMContext,
        *args,
        **kwargs
    ) -> None:
        async with state.proxy() as data:
            data['crypto_ticker'] = message.text

        await message.reply(self.is_current_data_state_text, reply_markup=get_is_current_data_kb())
        await PortfolioRecordCreationStatesGroup.is_current_data_will_be_used.set()

    async def create_portfolio_record__on_is_current_data_state(
        self,
        message: types.Message,
        state: FSMContext,
        *args,
        **kwargs
    ) -> None:
        async with state.proxy() as data:
            current_price_data: dict = (await get_current_price([data['crypto_ticker']]))
            current_price = current_price_data[data['crypto_ticker']]

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

    async def create_portfolio_record__on_action_date_state(
        self,
        message: types.Message,
        state: FSMContext,
        *args,
        **kwargs
    ) -> None:
        try:
            action_date = datetime.strptime(message.text, "%d/%m/%Y").date()
        except:
            await state.finish()
            await message.reply(text=self.wrong_date_text)
            return

        async with state.proxy() as data:
            data['action_date'] = action_date
            await message.reply(self.enter_price_text, reply_markup=get_cancel_kb())
            await PortfolioRecordCreationStatesGroup.by_price.set()

    async def create_portfolio_record__on_by_price_state(
        self,
        message: types.Message,
        state: FSMContext,
        *args,
        **kwargs
    ) -> None:
        async with state.proxy() as data:
            try:
                by_price: float = float(message.text)
            except:
                await state.finish()
                await message.reply(text=self.wrong_price_or_value_text)
                return

            data['by_price'] = by_price

            await message.reply("Тип операции:", reply_markup=get_action_type_kb())
            await PortfolioRecordCreationStatesGroup.action_type.set()

    async def create_portfolio_record__on_action_type_state(
        self,
        message: types.Message,
        state: FSMContext,
        *args,
        **kwargs
    ) -> None:
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

        await message.reply("Введите количество (целое число либо с пл.запятой)):", reply_markup=get_cancel_kb())
        await PortfolioRecordCreationStatesGroup.value.set()

    async def create_portfolio_record__on_value_state(
        self,
        message: types.Message,
        state: FSMContext,
        *args,
        **kwargs
    ) -> None:
        async with state.proxy() as data:
            try:
                value: float = float(message.text)
            except:
                await state.finish()
                await message.reply(text=self.wrong_price_or_value_text)
                return

            await self.portfolio_controller.create_portfolio_record(
                tg_id=message['from']['id'],
                crypto_ticker=data['crypto_ticker'],
                action_date=data['action_date'] if 'action_date' in data else None,
                action_type=data['action_type'],
                by_price=data['by_price'],
                value=value
            )

            await state.finish()
            await message.reply(text="Операция добавлена, данные портфеля обновлены!")

    def register_handlers(self, dispatcher: Dispatcher):
        dispatcher.register_message_handler(self.create_portfolio_record__start_state, commands=['create_record'])
        dispatcher.register_message_handler(
            self.create_portfolio_record__on_crypto_ticker_state,
            state=PortfolioRecordCreationStatesGroup.crypto_ticker
        )
        dispatcher.register_message_handler(
            self.create_portfolio_record__on_is_current_data_state,
            state=PortfolioRecordCreationStatesGroup.is_current_data_will_be_used
        )
        dispatcher.register_message_handler(
            self.create_portfolio_record__on_action_date_state,
            state=PortfolioRecordCreationStatesGroup.action_date
        )
        dispatcher.register_message_handler(
            self.create_portfolio_record__on_by_price_state,
            state=PortfolioRecordCreationStatesGroup.by_price
        )
        dispatcher.register_message_handler(
            self.create_portfolio_record__on_action_type_state,
            state=PortfolioRecordCreationStatesGroup.action_type
        )
        dispatcher.register_message_handler(
            self.create_portfolio_record__on_value_state,
            state=PortfolioRecordCreationStatesGroup.value
        )
