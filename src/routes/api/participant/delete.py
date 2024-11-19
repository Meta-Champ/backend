from src.core.database import get_async_session
from src.core.schema import Participant as ParticipantSchema
from src.middlewares import authenticate
from src.models.participant import Participant
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __400__, __403__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
participants = FastCRUD(ParticipantSchema)


@router.delete(
    path='/{id}',
    response_model=Participant,
    responses={
        400: __400__,
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Удаление участника',
    response_description='Участник удален',
)
async def request(
    id: int,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Participant | HTTPException:
    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN]:
        raise HTTPException(status_code=403, detail='Access denied')

    row: Participant | None = await participants.get(
        conn,
        id = id,
        schema_to_select=Participant,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Участник не найден')

    await participants.delete(db=conn, id=id)

    return row
