from src.core.database import get_async_session
from src.core.schema import (
    Protocol as ProtocolSchema,
    Direction as DirectionSchema,
    Participant as ParticipantSchema
)
from src.middlewares import authenticate
from src.models.protocol import Protocol, ProtocolCreate, ProtocolCreateInternal
from src.models.role import SystemRoles, DirectionRoles
from src.utils.documentation_statuses import __400__, __403__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
protocols = FastCRUD(ProtocolSchema)
directions = FastCRUD(DirectionSchema)
participants = FastCRUD(ParticipantSchema)


@router.post(
    path='/',
    response_model=Protocol,
    responses={
        400: __400__,
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Создание протокола',
    response_description='Протокол создан',
)
async def request(
    data: ProtocolCreate,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Protocol | HTTPException:
    if not await directions.exists(conn, id = data.direction_id):
        raise HTTPException(status_code=400, detail='Направление не найдено')

    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN] and \
        not await participants.exists(
            conn,
            id = user.id,
            direction_id = data.direction_id,
            role = DirectionRoles.CHIEF_EXPERT,
        ):
        raise HTTPException(status_code=403, detail='Access denied')

    return await protocols.create(
        db=conn,
        object=ProtocolCreateInternal(**{
            **data.model_dump(),
            'assigned_by': []
        })
    )
