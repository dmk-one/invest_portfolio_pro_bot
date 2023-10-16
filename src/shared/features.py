from typing import List, Iterable
from urllib.parse import quote

import aiohttp

from functools import wraps
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
    crypto_symbol_list: Iterable[str]
):
    url = 'https://api.coingecko.com/api/v3/simple/price?'

    ids_param = quote(','.join(crypto_symbol_list))
    url = f"{url}ids={ids_param}&vs_currencies=usd"

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            prices = await response.json()

            result = {}

            for crypto_symbol, price_data in prices.items():
                result[crypto_symbol] = price_data['usd']

            return result
