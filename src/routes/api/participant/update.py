from src.core.database import get_async_session
from src.core.schema import Participant as ParticipantSchema
from src.middlewares import authenticate
from src.models.participant import Participant, ParticipantUpdate
from src.models.role import SystemRoles, DirectionRoles
from src.utils.documentation_statuses import __400__, __403__, __404__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
participants = FastCRUD(ParticipantSchema)


@router.patch(
    path='/{id}',
    response_model=Participant,
    responses={
        400: __400__,
        403: __403__,
        404: __404__,
        500: __500__,
    },
    status_code=200,
    summary='Обновление участника',
    response_description='Участник обновлен',
)
async def request(
    id: int, 
    data: ParticipantUpdate,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Participant | HTTPException:
    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN]:
        raise HTTPException(status_code=403, detail='Access denied')

    row: Participant | None = await participants.get(
        conn,
        id=id,
        schema_to_select=Participant,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Участник не найден')

    await participants.update(db=conn, id=id, object=data)

    row.role = data.role

    return row
