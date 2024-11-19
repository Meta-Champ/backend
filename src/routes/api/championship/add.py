from src.core.database import get_async_session
from src.core.schema import Championship as ChampionshipSchema
from src.middlewares import authenticate
from src.models.championship import Championship, ChampionshipCreate
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __400__, __403__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
championships = FastCRUD(ChampionshipSchema)


@router.post(
    path='/',
    response_model=Championship,
    responses={
        400: __400__,
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Создание чемпионата',
    response_description='Чемпионат создан',
)
async def request(
    data: ChampionshipCreate,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Championship | HTTPException:
    if user.role != SystemRoles.OWNER:
        raise HTTPException(status_code=403, detail='Access denied')

    exist: bool | None = await championships.exists(conn, name = data.name)

    if exist:
        raise HTTPException(status_code=400, detail='Чемпионат с таким названием уже существует')

    return await championships.create(
        db=conn,
        object=ChampionshipCreate(**(data.model_dump()))
    )
