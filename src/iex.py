import requests

from src.abstractions import AbstractApiClient
from src.config import settings
from src.schemas import APICurrency


class IEXCloudClient(AbstractApiClient):

    def request(
            self,
            url: str,
            query_params: dict | None = None,
    ) -> APICurrency | None:
        try:
            response = requests.get(
                url,
                params=query_params,
                timeout=3,
            )
        except TimeoutError:
            return None

        if response.status_code != 200:
            return None

        data = response.json()[0]
        if data is None:
            return None

        api_currency = APICurrency(**data)
        return api_currency
