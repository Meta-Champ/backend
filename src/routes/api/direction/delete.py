from src.core.database import get_async_session
from src.core.schema import (
    Direction as DirectionSchema,
    Task as TaskSchema,
    Evaluation as EvaluationSchema,
    Participant as ParticipantSchema,
    Protocol as ProtocolSchema,
    Delivery as DeliverySchema
)
from src.middlewares import authenticate
from src.models.direction import Direction
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __400__, __403__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
directions = FastCRUD(DirectionSchema)
tasks = FastCRUD(TaskSchema)
evaluations = FastCRUD(EvaluationSchema)
participants = FastCRUD(ParticipantSchema)
protocols = FastCRUD(ProtocolSchema)
delivery = FastCRUD(DeliverySchema)


@router.delete(
    path='/{id}',
    response_model=Direction,
    responses={
        400: __400__,
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Удаление направления',
    response_description='Направление удалено',
)
async def request(
    id: int,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Direction | HTTPException:
    if user.role != SystemRoles.OWNER:
        raise HTTPException(status_code=403, detail='Access denied')

    row: Direction | None = await directions.get(
        conn,
        id = id,
        schema_to_select=Direction,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Направление не найдено')

    await tasks.delete(db=conn, direction_id=id, allow_multiple=True)
    await evaluations.delete(db=conn, direction_id=id, allow_multiple=True)
    await participants.delete(db=conn, direction_id=id, allow_multiple=True)
    await protocols.delete(db=conn, direction_id=id, allow_multiple=True)
    await delivery.delete(db=conn, direction_id=id, allow_multiple=True)
    await directions.delete(db=conn, id=id)

    return row
