from src.core.database import get_async_session
from src.core.schema import Championship as ChampionshipSchema
from src.middlewares import authenticate
from src.models.championship import Championship, ChampionshipUpdate
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __400__, __403__, __404__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
championships = FastCRUD(ChampionshipSchema)


@router.patch(
    path='/{id}',
    response_model=Championship,
    responses={
        400: __400__,
        403: __403__,
        404: __404__,
        500: __500__,
    },
    status_code=200,
    summary='Обновление чемпионата',
    response_description='Чемпионат обновлен',
)
async def request(
    id: int, 
    data: ChampionshipUpdate,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Championship | HTTPException:
    if user.role != SystemRoles.OWNER:
        raise HTTPException(status_code=403, detail='Access denied')

    row: Championship | None = await championships.get(
        conn,
        id = id,
        schema_to_select=Championship,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Чемпионат не найден')

    exist: Championship | None = await championships.get(
        conn,
        name = data.name,
        schema_to_select=Championship,
        return_as_model=True
    )

    if exist and exist.id != id:
        raise HTTPException(status_code=400, detail='Чемпионат с таким названием уже существует')

    return await championships.update(
        db=conn,
        id = id,
        object=ChampionshipUpdate(name=data.name),
        schema_to_select=Championship,
        return_as_model=True
    )
