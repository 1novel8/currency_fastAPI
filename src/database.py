from motor import motor_asyncio

from src.config import settings
from src.schemas import Currency

client = motor_asyncio.AsyncIOMotorClient(
    settings.MONGO_HOST,
    settings.MONGO_PORT,
)

db = client[settings.MONGO_DB]
trading_collection = db.trading_collection


class CurrencyRepository:
    collection = trading_collection

    async def create(self, currency: Currency) -> None:
        obj = await self.get_by_name_or_none(name=currency.name)
        if obj is not None:
            return None

        document = currency.model_dump()
        document['price_for_sale'] = [document['price_for_sale']]
        document['price_for_buy'] = [document['price_for_buy']]
        await self.collection.insert_one(document)

    async def get_by_name_or_none(self, name: str) -> dict | None:
        document = {'name': name}
        currency = await self.collection.find_one(document)
        return currency

    async def update(self, currency: Currency) -> Currency | None:
        obj = await self.get_by_name_or_none(name=currency.name)
        if obj is None:
            return None

        filter_ = {"name": currency.name}
        append = {
            "$push": {
                "price_for_sale": currency.price_for_sale,
                "price_for_buy": currency.price_for_buy,
            }
        }
        await self.collection.update_one(filter_, append)
        return currency

    async def list_of_names(self) -> list[str]:
        distinct_names = await self.collection.distinct('name')
        return distinct_names
