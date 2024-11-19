from src.core.database import get_async_session
from src.core.schema import Direction as DirectionSchema, Championship as ChampionshipSchema
from src.middlewares import authenticate
from src.models.direction import Direction, DirectionCreate
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __400__, __403__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
directions = FastCRUD(DirectionSchema)
championships = FastCRUD(ChampionshipSchema)


@router.post(
    path='/',
    response_model=Direction,
    responses={
        400: __400__,
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Создание направления',
    response_description='Направление создано',
)
async def request(
    data: DirectionCreate,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Direction | HTTPException:
    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN]:
        raise HTTPException(status_code=403, detail='Access denied')

    if not await championships.exists(conn, id = data.championship_id):
        raise HTTPException(status_code=404, detail='Чемпионат с предоставленным id не найден')

    exist: bool | None = await directions.exists(
        conn,
        championship_id = data.championship_id,
        name = data.name,
        is_juniors = data.is_juniors
    )

    if exist:
        raise HTTPException(status_code=400, detail='Направление с такими параметрами уже существует')

    return await directions.create(
        db=conn,
        object=DirectionCreate(**(data.model_dump()))
    )
