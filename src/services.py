import requests

from src.config import settings
from src.database import CurrencyRepository
from src.schemas import Currency, APICurrency


class CurrencyService:
    repository = CurrencyRepository()

    @staticmethod
    def fetch_currency_from_iex(name: str) -> Currency | None:
        api_key = settings.IEX_API_KEY
        url = f'https://api.iex.cloud/v1/data/core/quote/{name}?token={api_key}'
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()[0]
            api_currency = APICurrency(**data)
            currency = Currency.from_api(api_currency=api_currency)
            return currency
        return None

    async def create(self, name: str) -> None:
        currency = self.fetch_currency_from_iex(name=name)
        if currency:
            await self.repository.create(currency=currency)

    async def update(self, name: str) -> Currency | None:
        currency = self.fetch_currency_from_iex(name=name)
        if currency:
            return await self.repository.update(currency=currency)
        return None

    async def list_of_names(self) -> list[str]:
        return await self.repository.list_of_names()
