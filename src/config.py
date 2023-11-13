from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """ General settings for all project """

    CELERY_BROKER: str
    CELERY_RESULT_BACKEND: str
    FASTAPI_PORT: str
    FASTAPI_HOST: str
    MONGO_PORT: int
    MONGO_HOST: str
    MONGO_DB: str

    IEX_URL: str
    IEX_API_KEY: str

    ZOOKEEPER_CLIENT_PORT: str
    ZOOKEEPER_TICK_TIME: str

    KAFKA_BROKER_ID: str
    KAFKA_LISTENERS: str
    KAFKA_ADVERTISED_LISTENERS: str
    KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: str
    KAFKA_INTER_BROKER_LISTENER_NAME: str
    KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: int
    KAFKA_AUTO_CREATE_TOPICS_ENABLE: bool
    KAFKA_ZOOKEEPER_CONNECT: str
    KAFKA_CREATE_TOPICS: str
    KAFKA_URL: str

    REDIS_PORT: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
