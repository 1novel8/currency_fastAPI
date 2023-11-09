from src.database import CurrencyRepository
from src.iex.client import IEXCloudClient
from src.schemas import Currency


class CurrencyService:
    repository = CurrencyRepository()

    @staticmethod
    def fetch_currency_from_iex(name: str) -> Currency | None:
        api_currency = IEXCloudClient.request(name=name)
        if api_currency is not None:
            currency = Currency.from_api(api_currency=api_currency)
            return currency
        return None

    async def create(self, name: str) -> None:
        currency = self.fetch_currency_from_iex(name=name)
        if currency is not None:
            await self.repository.create(currency=currency)

    async def update(self, name: str) -> Currency | None:
        currency = self.fetch_currency_from_iex(name=name)
        if currency is not None:
            return await self.repository.update(currency=currency)
        return None

    async def list_of_names(self) -> list[str]:
        return await self.repository.list_of_names()
