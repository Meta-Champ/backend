from src.core.database import get_async_session
from src.core.schema import Championship as ChampionshipSchema
from src.middlewares import authenticate
from src.models.championship import Championship
from src.utils.documentation_statuses import __403__, __404__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
championships = FastCRUD(ChampionshipSchema)


@router.get(
    path='/{id}',
    response_model=Championship,
    responses={
        403: __403__,
        404: __404__,
        500: __500__,
    },
    status_code=200,
    summary='Получение чемпионата',
    response_description='Чемпионат получен',
)
async def request(
    id: int,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Championship | HTTPException:
    row: Championship | None = await championships.get(
        conn,
        id=id,
        schema_to_select=Championship,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Чемпионат не найден')

    return row
