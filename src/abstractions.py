from abc import ABC, abstractmethod

from pydantic import BaseModel


class AbstractApiClient(ABC):

    @property
    @abstractmethod
    def api_key(self):
        ...

    @classmethod
    @abstractmethod
    def request(cls, name: str):
        ...


class AbstractMongoRepository(ABC):
    @property
    @abstractmethod
    def collection(self):
        ...

    @abstractmethod
    async def create(self, model: BaseModel) -> None:
        ...

    @abstractmethod
    async def update(self, model: BaseModel) -> BaseModel | None:
        ...
