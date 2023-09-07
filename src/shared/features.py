import aiohttp

from functools import wraps
from bs4 import BeautifulSoup
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
    url = 'https://coinmarketcap.com/'

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            soup = BeautifulSoup(response.content, 'html.parser')
            data = soup.find('a', {'href': '/currencies/bitcoin/#markets'}).text

            data = data.replace(',', '')
            price = data.replace('$', '')

