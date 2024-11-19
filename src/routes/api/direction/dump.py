from src.core.database import get_async_session
from src.core.schema import Direction as DirectionSchema
from src.middlewares import authenticate
from src.models.direction import Direction, DirectionDump
from src.utils.documentation_statuses import __403__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
directions = FastCRUD(DirectionSchema)


@router.get(
    path='/',
    response_model=DirectionDump,
    responses={
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Получение направлений',
    response_description='Направления получены',
)
async def request(
    offset: int = 0,
    limit: int = 100,
    is_juniors: bool | None = None,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> DirectionDump | HTTPException:
    if offset < 0:
        raise HTTPException(status_code=400, detail='Значение offset не может быть меньше 0')
    
    if limit < 1:
        raise HTTPException(status_code=400, detail='Значение limit не может быть меньше 1')

    if limit > 100:
        raise HTTPException(status_code=400, detail='Значение limit не может быть больше 100')
    
    opts = {}

    if is_juniors is not None:
        opts['is_juniors'] = is_juniors

    return await directions.get_multi(
        conn,
        offset=offset,
        limit=limit,
        **opts,
        schema_to_select=Direction,
        return_as_model=True
    )
