from pydantic import BaseModel


class APICurrency(BaseModel):
    symbol: str
    iexAskPrice: float | None
    iexBidPrice: float | None
    latestPrice: float


class CurrencyDetail(BaseModel):
    name: str
    price_for_buy: float
    price_for_sale: float

    @classmethod
    def from_api(cls, api_currency: APICurrency):
        price_for_buy = api_currency.iexAskPrice
        price_for_sale = api_currency.iexBidPrice
        if price_for_buy == 0 or price_for_buy is None:
            price_for_buy = api_currency.latestPrice
        if price_for_sale == 0 or price_for_sale is None:
            price_for_sale = api_currency.latestPrice

        return cls(
            name=api_currency.symbol,
            price_for_buy=price_for_buy,
            price_for_sale=price_for_sale,
        )


class CurrencyFull(BaseModel):
    name: str
    price_for_buy_list: list[float]
    price_for_sale_list: list[float]

    @classmethod
    def from_detail(cls, currency_detail: CurrencyDetail):
        return cls(
            name=currency_detail.name,
            price_for_buy_list=[currency_detail.price_for_buy],
            price_for_sale_list=[currency_detail.price_for_sale],
        )
