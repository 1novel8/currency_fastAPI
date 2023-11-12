from typing import Optional

import pytest

from src.schemas import APICurrency, CurrencyDetail
from src.services import CurrencyService

api_currency_tsl = APICurrency(
        symbol='TSL',
        iexAskPrice=12,
        iexBidPrice=11,
        latestPrice=13,
)

api_currency_tsl_no_price = APICurrency(
        symbol='TSL',
        iexAskPrice=0,
        iexBidPrice=0,
        latestPrice=13,
)

detail_currency_tsl = CurrencyDetail(
        name='TSL',
        price_for_sale=11,
        price_for_buy=12,
)


@pytest.mark.asyncio
async def test_fetch_currency_from_iex(mock_iexcloud_request) -> None:
    service = CurrencyService()
    mock_iexcloud_request.return_value = api_currency_tsl

    currency = service.fetch_currency_from_iex('TSL')

    assert currency is not None
    assert currency.name == 'TSL'
    assert currency.price_for_buy == 12
    assert currency.price_for_sale == 11


@pytest.mark.asyncio
async def test_fetch_currency_from_iex_no_price(mock_iexcloud_request) -> None:
    service = CurrencyService()
    mock_iexcloud_request.return_value = api_currency_tsl_no_price

    currency = service.fetch_currency_from_iex('TSL')

    assert currency is not None
    assert currency.name == 'TSL'
    assert currency.price_for_buy == 13
    assert currency.price_for_sale == 13


@pytest.mark.asyncio
async def test_fetch_currency_from_iex_failure(mock_iexcloud_request) -> None:
    service = CurrencyService()
    mock_iexcloud_request.return_value = None

    currency: Optional[CurrencyDetail] = service.fetch_currency_from_iex('unknown_currency')
    assert currency is None


@pytest.mark.asyncio
async def test_currency_create(
        mock_create_currency,
        mock_iexcloud_request,
        mock_get_currency_by_name
) -> None:
    service = CurrencyService()
    mock_iexcloud_request.return_value = api_currency_tsl
    mock_get_currency_by_name.return_value = None
    mock_create_currency.return_value = detail_currency_tsl

    currency: Optional[CurrencyDetail] = await service.create(name='TSL')

    assert currency is not None
    assert currency.name == 'TSL'
    assert currency.price_for_buy == api_currency_tsl.iexAskPrice
    assert currency.price_for_sale == api_currency_tsl.iexBidPrice


@pytest.mark.asyncio
async def test_currency_create_failure(mock_iexcloud_request, mock_get_currency_by_name) -> None:
    service = CurrencyService()
    mock_iexcloud_request.return_value = api_currency_tsl
    mock_get_currency_by_name.return_value = {'_id': 12, 'name': 'TSL'}

    currency: Optional[CurrencyDetail] = await service.create(name='TSL')

    assert currency is None


@pytest.mark.asyncio
async def test_currency_update(
        mock_update_currency,
        mock_iexcloud_request,
        mock_get_currency_by_name
) -> None:
    service = CurrencyService()
    mock_iexcloud_request.return_value = api_currency_tsl
    mock_get_currency_by_name.return_value = {'_id': 12, 'name': 'TSL'}
    mock_update_currency.return_value = detail_currency_tsl

    currency: Optional[CurrencyDetail] = await service.update(name='TSL')
    assert currency is not None
    assert currency.name == 'TSL'
    assert currency.price_for_buy == api_currency_tsl.iexAskPrice
    assert currency.price_for_sale == api_currency_tsl.iexBidPrice


@pytest.mark.asyncio
async def test_currency_update_failure(mock_iexcloud_request, mock_get_currency_by_name) -> None:
    service = CurrencyService()
    mock_iexcloud_request.return_value = api_currency_tsl
    mock_get_currency_by_name.return_value = None
    currency: Optional[CurrencyDetail] = await service.update(name='TSL')

    assert currency is None
