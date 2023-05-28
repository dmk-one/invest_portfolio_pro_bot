from os import getenv

DB_HOST = getenv('DB_HOST')
DB_NAME = getenv('DB_NAME')
DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')
DB_PORT = getenv('DB_PORT')

SQLALCHEMY_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
ASYNC_SQLALCHEMY_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

SQLALCHEMY_ECHO = False
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_MAX_OVERFLOW = 5

BOT_TOKEN_API = getenv('BOT_TOKEN_API')

CoinAPI_KEY = getenv('CoinAPI_KEY')
