from enum import Enum


class MerchantPermission(Enum):
    CATALOG = 'CATALOG'
    ORDER = 'ORDER'
    COMMAND = 'COMMAND'
    LOGISTIC = 'LOGISTIC'
    MERCHANT = 'MERCHANT'
    INTEGRATION = 'INTEGRATION'