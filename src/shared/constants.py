from enum import IntEnum


class ROLE(IntEnum):
    CUSTOMER = 1
    ADMIN = 2
    MODERATOR = 3


class ActionType(IntEnum):
    BUY = 0
    SELL = 1
