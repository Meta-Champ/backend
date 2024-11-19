from src.core.database import get_async_session
from src.core.schema import (
    Evaluation as EvaluationSchema,
    Participant as ParticipantSchema
)
from src.middlewares import authenticate
from src.models.evaluation import Evaluation
from src.models.role import SystemRoles, DirectionRoles
from src.utils.documentation_statuses import __400__, __403__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
evaluations = FastCRUD(EvaluationSchema)
participants = FastCRUD(ParticipantSchema)


@router.delete(
    path='/{id}',
    response_model=Evaluation,
    responses={
        400: __400__,
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Удаление оценки',
    response_description='Оценка удалена',
)
async def request(
    id: int,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Evaluation | HTTPException:
    row: Evaluation | None = await evaluations.get(
        conn,
        id = id,
        schema_to_select=Evaluation,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Оценка не найдена')
    
    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN] and \
        not await participants.exists(
            conn,
            user_id=user.id,
            direction_id=row.direction_id,
            role=DirectionRoles.CHIEF_EXPERT
        ):
        raise HTTPException(status_code=403, detail='Access denied')

    await evaluations.delete(db=conn, id=id)

    return row
