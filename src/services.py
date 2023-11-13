from src.iex import IEXCloudClient
from src.repositories import CurrencyRepository
from src.schemas import CurrencyDetail


class CurrencyService:
    repository = CurrencyRepository()

    @staticmethod
    def fetch_currency_from_iex(name: str) -> CurrencyDetail | None:
        api_currency = IEXCloudClient.request(name=name)
        if api_currency is not None:
            currency = CurrencyDetail.from_api(api_currency=api_currency)
            return currency
        return None

    async def create(self, name: str) -> CurrencyDetail | None:
        currency = self.fetch_currency_from_iex(name=name)
        if currency is None:
            return None

        obj = await self.get_by_name(name=currency.name)
        if obj is not None:
            return None

        await self.repository.create(model=currency)
        return currency

    async def update(self, name: str) -> CurrencyDetail | None:
        currency = self.fetch_currency_from_iex(name=name)

        if currency is None:
            return None

        obj = await self.get_by_name(name=currency.name)
        if obj is None:
            return None

        await self.repository.update(model=currency)
        return currency

    async def list_of_names(self) -> list[str]:
        return await self.repository.list_of_names()

    async def get_by_name(self, name: str) -> dict | None:
        currency = await self.repository.get_by_name(name=name)
        return currency
