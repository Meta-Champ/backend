from src.core.database import get_async_session
from src.core.schema import Evaluation as EvaluationSchema
from src.core.schema import Participant as ParticipantSchema
from src.middlewares import authenticate
from src.models.evaluation import Evaluation, EvaluationDump
from src.models.role import SystemRoles, DirectionRoles
from src.models.participant import Participant
from src.utils.documentation_statuses import __403__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
evaluations = FastCRUD(EvaluationSchema)
participants = FastCRUD(ParticipantSchema)


@router.get(
    path='/participant/{id}',
    response_model=EvaluationDump,
    responses={
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Получение оценок',
    response_description='Оценки получены',
)
async def request(
    id: int,
    direction_id: int,
    offset: int = 0,
    limit: int = 100,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> EvaluationDump | HTTPException:
    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN] and \
        not await participants.exists(
            conn,
            user=user.id,
            direction_id=direction_id,
            role=DirectionRoles.CHIEF_EXPERT
        ):
        raise HTTPException(status_code=403, detail='Access denied')
    
    if not await participants.exists(conn, user=id, direction_id=direction_id):
        raise HTTPException(status_code=400, detail='Участник не найден')

    if offset < 0:
        raise HTTPException(status_code=400, detail='Значение offset не может быть меньше 0')
    
    if limit < 1:
        raise HTTPException(status_code=400, detail='Значение limit не может быть меньше 1')

    if limit > 100:
        raise HTTPException(status_code=400, detail='Значение limit не может быть больше 100')

    return await evaluations.get_multi(
        conn,
        offset=offset,
        limit=limit,
        user_id=id,
        direction_id=direction_id,
        schema_to_select=Evaluation,
        return_as_model=True
    )
