from enum import Enum


class ModulePermissions(Enum):
    MERCHANT = 'MERCHANT'
    INTEGRATION = 'INTEGRATION'
    PRODUCTS = 'PRODUCTS'
    ORDERS = 'ORDERS'
    COMMANDS = 'COMMANDS'
    ROUTES = 'ROUTES'
    DRIVERS = 'DRIVERS'
    CATALOGS = 'CATALOGS'