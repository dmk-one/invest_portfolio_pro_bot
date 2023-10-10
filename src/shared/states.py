from aiogram.dispatcher.filters.state import StatesGroup, State


class PortfolioRecordCreationStatesGroup(StatesGroup):
    crypto_ticker = State()
    is_current_data_will_be_used = State()
    action_date = State()
    action_type = State()
    by_price = State()
    value = State()
