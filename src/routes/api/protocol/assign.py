from src.core.database import get_async_session
from src.core.schema import (
    Protocol as ProtocolSchema,
    Participant as ParticipantSchema
)
from src.middlewares import authenticate
from src.models.protocol import Protocol, ProtocolStatus
from src.utils.documentation_statuses import __400__, __403__, __404__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
protocols = FastCRUD(ProtocolSchema)
participants = FastCRUD(ParticipantSchema)


@router.post(
    path='/assign/{id}',
    response_model=Protocol,
    responses={
        400: __400__,
        403: __403__,
        404: __404__,
        500: __500__,
    },
    status_code=200,
    summary='Подписание протокола',
    response_description='Протокол подписан',
)
async def request(
    id: int,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Protocol | HTTPException:
    row: Protocol | None = await protocols.get(
        conn,
        id = id,
        schema_to_select=Protocol,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Протокол не найден')
    
    if user.id in row.assigned_by:
        raise HTTPException(status_code=400, detail='Протокол уже подписан')

    if not await participants.exists(
        conn,
        id = user.id,
        direction_id = row.direction_id,
    ):
        raise HTTPException(status_code=403, detail='Access denied')

    participants_count = await participants.count(conn, direction_id = row.direction_id)

    obj = {
        'assigned_by': [user.id] + row.assigned_by,
        'status': ProtocolStatus.ASSIGNED if participants_count == len([user.id] + row.assigned_by) else ProtocolStatus.PENDING
    }

    await protocols.update(db=conn, id = id, object=obj)

    return Protocol(**{ **row.model_dump(), **obj })
