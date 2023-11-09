from fastapi import APIRouter, Response, status

from src.services import CurrencyService

router = APIRouter(prefix='', tags=['core'])


@router.get('/health')
def health():
    return Response(status_code=status.HTTP_200_OK)


@router.get('/test')
async def test():
    service = CurrencyService()
    await service.create('tsl')
    return Response(status_code=status.HTTP_200_OK)
