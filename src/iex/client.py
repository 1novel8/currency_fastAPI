import requests

from src.base.abstractions import AbstractApiClient
from src.config import settings
from src.schemas import APICurrency


class IEXCloudClient(AbstractApiClient):
    api_key = settings.IEX_API_KEY

    @classmethod
    def request(cls, name: str) -> APICurrency | None:
        url = f'https://api.iex.cloud/v1/data/core/quote/{name}'
        response = requests.get(
            url,
            params={'token': cls.api_key},
            timeout=3
        )
        if response.status_code == 200:
            data = response.json()[0]
            api_currency = APICurrency(**data)
            return api_currency
        return None
