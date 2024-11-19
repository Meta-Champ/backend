from src.core.database import get_async_session
from src.core.schema import (
    Direction as DirectionSchema,
    Participant as ParticipantSchema,
    User as UserSchema
)
from src.middlewares import authenticate
from src.models.participant import Participant, ParticipantCreate
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __400__, __403__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
directions = FastCRUD(DirectionSchema)
participants = FastCRUD(ParticipantSchema)
users = FastCRUD(UserSchema)


@router.post(
    path='/',
    response_model=Participant,
    responses={
        400: __400__,
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Создание участника',
    response_description='Участник создан',
)
async def request(
    data: ParticipantCreate,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Participant | HTTPException:
    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN]:
        raise HTTPException(status_code=403, detail='Access denied')

    if not await directions.exists(conn, id = data.direction_id):
        raise HTTPException(status_code=404, detail='Направление с предоставленным id не найдено')

    if not await users.exists(conn, id = data.user_id):
        raise HTTPException(status_code=404, detail='Пользователь с предоставленным id не найден')

    exist: bool | None = await participants.exists(
        conn,
        direction_id = data.direction_id,
        user_id = data.user_id
    )

    if exist:
        raise HTTPException(status_code=400, detail='Участник с такими параметрами уже существует')

    return await participants.create(
        db=conn,
        object=ParticipantCreate(**(data.model_dump()))
    )
