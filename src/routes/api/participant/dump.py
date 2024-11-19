from src.core.database import get_async_session
from src.core.schema import (
    Participant as ParticipantSchema,
    Direction as DirectionSchema
)
from src.middlewares import authenticate
from src.models.participant import Participant, ParticipantDump
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __403__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
participants = FastCRUD(ParticipantSchema)
directions = FastCRUD(DirectionSchema)


@router.get(
    path='/direction/{id}',
    response_model=ParticipantDump,
    responses={
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Получение участников',
    response_description='Участники получены',
)
async def request(
    id: int,
    offset: int = 0,
    limit: int = 100,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> ParticipantDump | HTTPException:
    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN] or \
        user.role == SystemRoles.USER and not await participants.exists(conn, user=user.id, direction_id=id):
        raise HTTPException(status_code=403, detail='Access denied')

    if not await directions.exists(conn, id=id):
        raise HTTPException(status_code=404, detail='Направление не найдено')

    if offset < 0:
        raise HTTPException(status_code=400, detail='Значение offset не может быть меньше 0')
    
    if limit < 1:
        raise HTTPException(status_code=400, detail='Значение limit не может быть меньше 1')

    if limit > 100:
        raise HTTPException(status_code=400, detail='Значение limit не может быть больше 100')

    return await participants.get_multi(
        conn,
        offset=offset,
        limit=limit,
        direction_id=id,
        schema_to_select=Participant,
        return_as_model=True
    )
