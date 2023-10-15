from typing import List
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


# async def _get_price_data(
#     session,
#     crypto_ticker: str,
#     page: int
# ):
#     crypto_ticker = crypto_ticker.upper()
#
#     url = f'https://www.coingecko.com/ru?page={page}'
#
#     async with session.get(url=url) as response:
#         res_content = await response.text()
#         soup = BeautifulSoup(res_content, 'lxml')
#         coingecko_table = soup.find('div', class_='coingecko-table')
#         tbody = coingecko_table.find('tbody')
#
#         for tr in tbody.find_all('tr'):
#             symbol = (tr.find('span', class_='d-lg-inline font-normal text-3xs tw-ml-0 md:tw-ml-2 md:tw-self-center tw-text-gray-500 dark:tw-text-white dark:tw-text-opacity-60')).text
#
#             td = tr.find('td', class_='td-price price text-right')
#             price = (td.find('span', class_='no-wrap')).text
#
#             if crypto_ticker in symbol:
#                 price = price.replace('$', '')
#                 price = price.replace(',', '.')
#                 return float(price)
#
#
# async def get_current_price(crypto_ticker: str) -> float:
#     async with aiohttp.ClientSession() as session:
#         results = await asyncio.gather(
#             *[_get_price_data(session, crypto_ticker, page) for page in range(1, 31)]
#         )
#
#     for result in results:
#         if result:
#             return result


async def _get_coins_list(
    session
):
    url = 'https://api.coingecko.com/api/v3/coins/list?include_platform=false'

    async with session.get(url=url) as response:
        return await response.json()


async def _get_coins_price(
    session,
    crypto_id_list: List[str]
):
    url = 'https://api.coingecko.com/api/v3/simple/price?'

    ids_param = quote(','.join(crypto_id_list))
    url = f"{url}ids={ids_param}&vs_currencies=usd"

    async with session.get(url=url) as response:
        return await response.json()


async def get_current_price(
    crypto_symbol_list: List[str]
):
    async with aiohttp.ClientSession() as session:
        # coins_list = await _get_coins_list(session)

        # symbol_id = {}
        # result = {}
        #
        # for symbol in crypto_symbol_list:
        #     for coin_data in coins_list:
        #         if coin_data['symbol'] == symbol.lower():
        #             symbol_id[coin_data['id']] = symbol
        #
        # print('\n2', symbol_id)
        #
        # prices = await _get_coins_price(session, [_id for _id, symbol in symbol_id.items()])
        prices = await _get_coins_price(session, crypto_symbol_list)

        # for _id, price in prices:
        #     result[symbol_id[_id]] = price['usd']

        return prices
