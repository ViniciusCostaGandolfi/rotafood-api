from typing import List
from custom_model import BaseModel, HttpUrl

class Campaign(BaseModel):
    id: str
    name: str


class Sponsorship(BaseModel):
    name: str
    value: float
    description: str

class Benefit(BaseModel):
    targetId: str
    sponsorshipValues: List[Sponsorship]
    value: float
    target: str
    campaign: Campaign

class Campaign(BaseModel):
    id: str
    name: str

class DigitalWalletInformation(BaseModel):
    name: str

class CashInformation(BaseModel):
    changeFor: float

class CreditCardInformation(BaseModel):
    brand: str

class PaymentMethod(BaseModel):
    wallet: DigitalWalletInformation
    method: str
    prepaid: bool
    currency: str
    type: str
    value: float
    cash: CashInformation
    card: CreditCardInformation

class Payments(BaseModel):
    methods: List[PaymentMethod]
    pending: float
    prepaid: float

class ScalePrice(BaseModel):
    minQuantity: int
    price: float

class ItemScalePrices(BaseModel):
    defaultPrice: float
    scales: List[ScalePrice]

class ItemOption(BaseModel):
    unitPrice: float
    unit: str
    ean: str
    quantity: int
    externalCode: str
    price: float
    name: str
    index: int
    id: str
    addition: float

class Item(BaseModel):
    unitPrice: float
    quantity: int
    externalCode: str
    totalPrice: float
    index: int
    unit: str
    ean: str
    price: float
    scalePrices: ItemScalePrices
    observations: str
    imageUrl: HttpUrl
    name: str
    options: List[ItemOption]
    id: str
    optionsPrice: float

class Liability(BaseModel):
    name: str
    percentage: float

class AdditionalFee(BaseModel):
    type: str
    value: float
    description: str
    fullDescription: str
    liabilities: List[Liability]

class Coordinates(BaseModel):
    latitude: float
    longitude: float

class DeliveryAddress(BaseModel):
    reference: str
    country: str
    streetName: str
    formattedAddress: str
    streetNumber: str
    city: str
    postalCode: str
    coordinates: Coordinates
    neighborhood: str
    state: str
    complement: str

class DeliveryInformation(BaseModel):
    mode: str
    pickupCode: str
    deliveredBy: str
    deliveryAddress: DeliveryAddress
    deliveryDateTime: str

class ScheduleInformation(BaseModel):
    deliveryDateTimeStart: str
    deliveryDateTimeEnd: str

class IndoorInformation(BaseModel):
    mode: str
    deliveryDateTime: str
    table: str

class TakeoutInformation(BaseModel):
    mode: str
    takeoutDateTime: str

class Phone(BaseModel):
    number: str
    localizer: str
    localizerExpiration: str

class Customer(BaseModel):
    phone: Phone
    documentNumber: str
    name: str
    ordersCountOnMerchant: int
    segmentation: str
    id: str

class Total(BaseModel):
    benefits: float
    deliveryFee: float
    orderAmount: float
    subTotal: float
    additionalFees: float

class Picking(BaseModel):
    picker: str
    replacementOptions: List[str]

class Merchant(BaseModel):
    name: str
    id: str

class Benefits(BaseModel):
    benefits: List[Benefit]

class IFoodOrderDetailDto(BaseModel):
    description: str
    benefits: Benefits
    orderType: str
    payments: Payments
    merchant: Merchant
    salesChannel: str
    picking: Picking
    orderTiming: str
    createdAt: str
    total: Total
    preparationStartDateTime: str
    id: str
    displayId: str
    items: List[Item]
    customer: Customer
    extraInfo: str
    additionalFees: List[AdditionalFee]
    delivery: DeliveryInformation
    schedule: ScheduleInformation
    indoor: IndoorInformation
    takeout: TakeoutInformation
