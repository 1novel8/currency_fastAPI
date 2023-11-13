from src.abstractions import AbstractMongoRepository
from src.database import trading_collection
from src.schemas import CurrencyDetail, CurrencyFull


class CurrencyRepository(AbstractMongoRepository):
    collection = trading_collection

    async def create(self, model: CurrencyDetail) -> None:
        currency_full = CurrencyFull.from_detail(currency_detail=model)
        await self.collection.insert_one(currency_full.model_dump())

    async def get_by_name(self, name: str) -> dict | None:
        document = {'name': name}
        currency = await self.collection.find_one(document)
        return currency

    async def update(self, model: CurrencyDetail) -> None:
        filter_ = {"name": model.name}
        append = {
            "$push": {
                "price_for_sale": model.price_for_sale,
                "price_for_buy": model.price_for_buy,
            }
        }
        await self.collection.update_one(filter_, append)

    async def list_of_names(self) -> list[str]:
        distinct_names = await self.collection.distinct('name')
        return distinct_names
