from src.core.database import get_async_session
from src.core.schema import Participant as ParticipantSchema
from src.middlewares import authenticate
from src.models.participant import Participant
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __403__, __404__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
participants = FastCRUD(ParticipantSchema)


@router.get(
    path='/{id}',
    response_model=Participant,
    responses={
        403: __403__,
        404: __404__,
        500: __500__,
    },
    status_code=200,
    summary='Получение участника',
    response_description='Участник получен',
)
async def request(
    id: int,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Participant | HTTPException:
    row: Participant | None = await participants.get(
        conn,
        id=id,
        schema_to_select=Participant,
        return_as_model=True
    )

    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN] or \
        not await participants.exists(conn, id=user.id, direction_id=row.direction_id):
        raise HTTPException(status_code=403, detail='Access denied')

    if not row:
        raise HTTPException(status_code=404, detail='Участник не найден')

    return row
