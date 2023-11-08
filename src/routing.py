from fastapi import APIRouter, Response, status

router = APIRouter(prefix='', tags=['core'])


@router.get('/health')
def health():
    return Response(status_code=status.HTTP_200_OK)
