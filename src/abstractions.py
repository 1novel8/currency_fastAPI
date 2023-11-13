from abc import ABC, abstractmethod

from pydantic import BaseModel


class AbstractApiClient(ABC):

    @abstractmethod
    def request(self, url: str, query_params: dict | None):
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
