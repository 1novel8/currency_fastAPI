from fastapi import APIRouter, Response, status

from src.services import CurrencyService

router = APIRouter(prefix='', tags=['core'])


@router.get('/health')
def health():
    return Response(status_code=status.HTTP_200_OK)


@router.get('/test')
def test():
    service = CurrencyService()
    service.fetch_currency_from_iex('tsl')
    return Response(status_code=status.HTTP_200_OK)
