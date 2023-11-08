from pydantic import BaseModel


class Currency(BaseModel):
    name: str
    price_for_buy: float
    price_for_sale: float


class CurrencyFull(BaseModel):
    name: str
    price_for_buy: list[float]
    price_for_sale: list[float]
