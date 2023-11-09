from motor import motor_asyncio

from src.abstractions import AbstractMongoRepository
from src.config import settings
from src.schemas import CurrencyDetail, CurrencyFull

client = motor_asyncio.AsyncIOMotorClient(
    settings.MONGO_HOST,
    settings.MONGO_PORT,
)

db = client[settings.MONGO_DB]
trading_collection = db.trading_collection


class CurrencyRepository(AbstractMongoRepository):
    collection = trading_collection

    async def create(self, model: CurrencyDetail) -> None:
        obj = await self.get_by_name_or_none(name=model.name)
        if obj is not None:
            return None

        currency_full = CurrencyFull.from_detail(currency_detail=model)
        await self.collection.insert_one(currency_full.model_dump())

    async def get_by_name_or_none(self, name: str) -> dict | None:
        document = {'name': name}
        currency = await self.collection.find_one(document)
        return currency

    async def update(self, model: CurrencyDetail) -> CurrencyDetail | None:
        obj = await self.get_by_name_or_none(name=model.name)
        if obj is None:
            return None

        filter_ = {"name": model.name}
        append = {
            "$push": {
                "price_for_sale": model.price_for_sale,
                "price_for_buy": model.price_for_buy,
            }
        }
        await self.collection.update_one(filter_, append)
        return model

    async def list_of_names(self) -> list[str]:
        distinct_names = await self.collection.distinct('name')
        return distinct_names
