import pytest

from src.iex import IEXCloudClient
from src.repositories import CurrencyRepository


@pytest.fixture
def mock_iexcloud_request(mocker):
    return mocker.patch.object(IEXCloudClient, 'request')


@pytest.fixture
def mock_get_currency_by_name(mocker):
    return mocker.patch.object(CurrencyRepository, 'get_by_name_or_none')


@pytest.fixture
def mock_create_currency(mocker):
    return mocker.patch.object(CurrencyRepository, 'create')


@pytest.fixture
def mock_update_currency(mocker):
    return mocker.patch.object(CurrencyRepository, 'update')
