from abc import ABC, abstractmethod


class AbstractApiClient(ABC):

    @classmethod
    @abstractmethod
    def request(cls, name: str):
        ...
