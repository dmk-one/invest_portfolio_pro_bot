import aiohttp

from functools import wraps

from settings import CoinAPI_KEY
from src.exceptions.shared import RoleException
from src.models import User


def set_role_validator(allowed_role_list: list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user: User = kwargs['user']

            if '*' in allowed_role_list or user.role in allowed_role_list:
                return func(*args, **kwargs)

            raise RoleException()

        return wrapper

    return decorator


async def get_current_price(
    crypto_abbreviation: str,
    quote: str = 'USDT',
    exchange: str = 'BINANCE'
):
    url = f'https://rest.coinapi.io/v1/symbols?' \
          f'filter_exchange_id={exchange}&' \
          f'filter_asset_id={crypto_abbreviation}'
    headers = {'X-CoinAPI-Key': CoinAPI_KEY}

    async with aiohttp.ClientSession() as session:
        async with session.get(
                url=url,
                headers=headers
        ) as response:
            for res in await response.json():
                if res['asset_id_quote'] == quote:
                    return res['price']
