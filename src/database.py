from motor import motor_asyncio

from src.config import settings

client = motor_asyncio.AsyncIOMotorClient(
    settings.MONGO_HOST,
    settings.MONGO_PORT,
)

db = client[settings.MONGO_DB]
trading_collection = db.trading_collection
