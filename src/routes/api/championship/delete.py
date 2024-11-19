from src.core.database import get_async_session
from src.core.schema import (
    Championship as ChampionshipSchema,
    Direction as DirectionSchema,
    Task as TaskSchema,
    Evaluation as EvaluationSchema,
    Participant as ParticipantSchema,
    Protocol as ProtocolSchema,
    Delivery as DeliverySchema
)
from src.middlewares import authenticate
from src.models.championship import Championship
from src.models.role import SystemRoles
from src.models.direction import Direction
from src.utils.documentation_statuses import __400__, __403__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
championships = FastCRUD(ChampionshipSchema)
directions = FastCRUD(DirectionSchema)
tasks = FastCRUD(TaskSchema)
evaluations = FastCRUD(EvaluationSchema)
participants = FastCRUD(ParticipantSchema)
protocols = FastCRUD(ProtocolSchema)
delivery = FastCRUD(DeliverySchema)


@router.delete(
    path='/{id}',
    response_model=Championship,
    responses={
        400: __400__,
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Удаление чемпионата',
    response_description='Чемпионат удален',
)
async def request(
    id: int,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Championship | HTTPException:
    if user.role != SystemRoles.OWNER:
        raise HTTPException(status_code=403, detail='Access denied')

    row: Championship | None = await championships.get(
        conn,
        id = id,
        schema_to_select=Championship,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Чемпионат не найден')

    for direction in await directions.get_multi(db=conn, championship_id=id, schema_to_select=Direction, return_as_model=True):
        await tasks.delete(db=conn, direction_id=direction.id, allow_multiple=True)
        await evaluations.delete(db=conn, direction_id=direction.id, allow_multiple=True)
        await participants.delete(db=conn, direction_id=direction.id, allow_multiple=True)
        await protocols.delete(db=conn, direction_id=direction.id, allow_multiple=True)
        await delivery.delete(db=conn, direction_id=direction.id, allow_multiple=True)
        await directions.delete(db=conn, id=direction.id)

    await championships.delete(db=conn, id=id)

    return row
