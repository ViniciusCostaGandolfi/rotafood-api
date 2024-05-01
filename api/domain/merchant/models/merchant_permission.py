from enum import Enum


class MerchantPermission(Enum):
    CATALOG = 'CATALOG'
    ORDERS = 'ORDERS'
    COMMAND = 'COMMAND'
    LOGISTIC = 'LOGISTIC'
    MERCHANT = 'MERCHANT'
    INTEGRATION = 'INTEGRATION'