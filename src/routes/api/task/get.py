from src.core.database import get_async_session
from src.core.schema import (
    Task as TaskSchema,
    Participant as ParticipantSchema
)
from src.middlewares import authenticate
from src.models.task import Task
from src.models.role import SystemRoles, DirectionRoles
from src.models.participant import Participant
from src.utils.documentation_statuses import __403__, __404__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
tasks = FastCRUD(TaskSchema)
participants = FastCRUD(ParticipantSchema)


@router.get(
    path='/{id}',
    response_model=Task,
    responses={
        403: __403__,
        404: __404__,
        500: __500__,
    },
    status_code=200,
    summary='Получение задачи',
    response_description='Задача получена',
)
async def request(
    id: int,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Task | HTTPException:
    row: Task | None = await tasks.get(
        conn,
        id=id,
        schema_to_select=Task,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Задача не найдена')

    participant: bool = await participants.get(
        conn,
        id = user.id,
        direction_id = row.direction_id,
        schema_to_select=Participant,
        return_as_model=True
    )

    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN] or \
        participant and participant.role != DirectionRoles.CHIEF_EXPERT:
        raise HTTPException(status_code=403, detail='Access denied')

    return row
