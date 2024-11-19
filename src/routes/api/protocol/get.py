from src.core.database import get_async_session
from src.core.schema import (
    Protocol as ProtocolSchema,
    Participant as ParticipantSchema
)
from src.middlewares import authenticate
from src.models.protocol import Protocol
from src.models.role import SystemRoles
from src.models.participant import Participant
from src.utils.documentation_statuses import __403__, __404__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
protocols = FastCRUD(ProtocolSchema)
participants = FastCRUD(ParticipantSchema)


@router.get(
    path='/{id}',
    response_model=Protocol,
    responses={
        403: __403__,
        404: __404__,
        500: __500__,
    },
    status_code=200,
    summary='Получение протокола',
    response_description='Протокол получен',
)
async def request(
    id: int,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Protocol | HTTPException:
    row: Protocol | None = await protocols.get(
        conn,
        id=id,
        schema_to_select=Protocol,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Протокол не найден')

    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN] or \
        not await participants.exists(
            conn,
            id = user.id,
            direction_id = row.direction_id,
            schema_to_select=Participant,
            return_as_model=True
        ):
        raise HTTPException(status_code=403, detail='Access denied')

    return row
