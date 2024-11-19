from src.core.database import get_async_session
from src.core.schema import Championship as ChampionshipSchema
from src.middlewares import authenticate
from src.models.championship import Championship, ChampionshipDump
from src.utils.documentation_statuses import __403__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
championships = FastCRUD(ChampionshipSchema)


@router.get(
    path='/',
    response_model=ChampionshipDump,
    responses={
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Получение чемпионата',
    response_description='Чемпионат получен',
)
async def request(
    offset: int = 0,
    limit: int = 100,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> ChampionshipDump | HTTPException:
    if offset < 0:
        raise HTTPException(status_code=400, detail='Значение offset не может быть меньше 0')
    
    if limit < 1:
        raise HTTPException(status_code=400, detail='Значение limit не может быть меньше 1')

    if limit > 100:
        raise HTTPException(status_code=400, detail='Значение limit не может быть больше 100')
    
    return await championships.get_multi(
        conn,
        offset=offset,
        limit=limit,
        schema_to_select=Championship,
        return_as_model=True
    )
