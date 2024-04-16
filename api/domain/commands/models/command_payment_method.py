
from enum import Enum


class CommandPaymentMethod(Enum):
    CASH = 'CASH'
    PIX = 'PIX'
    CREDIT_CARD = 'CREDIT_CARD'
    DEBIT_CARD = 'DEBIT_CARD'
    