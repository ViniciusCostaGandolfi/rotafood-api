from sqlalchemy import Enum


class OrderIndoorMode(Enum):
    DEFAULT = "DEFAULT"
    TABLE = "TABLE"