from src.core.database import get_async_session
from src.core.schema import (
    Evaluation as EvaluationSchema,
    Task as TaskSchema,
    User as UserSchema,
    Participant as ParticipantSchema,
    Direction as DirectionSchema
)
from src.middlewares import authenticate
from src.models.evaluation import Evaluation, EvaluationCreate
from src.models.role import SystemRoles, DirectionRoles
from src.models.task import Task
from src.models.participant import Participant
from src.utils.documentation_statuses import __400__, __403__, __409__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()

evaluations = FastCRUD(EvaluationSchema)
tasks = FastCRUD(TaskSchema)
users = FastCRUD(UserSchema)
participants = FastCRUD(ParticipantSchema)
directions = FastCRUD(DirectionSchema)


@router.post(
    path='/',
    response_model=Evaluation,
    responses={
        400: __400__,
        403: __403__,
        409: __409__,
        500: __500__,
    },
    status_code=200,
    summary='Создание оценки',
    response_description='Оценка создана',
)
async def request(
    data: EvaluationCreate,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Evaluation | HTTPException:
    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN] or \
        await participants.get(
            conn,
            user_id = user.id,
            direction_id = data.direction_id,
            role = DirectionRoles.CHIEF_EXPERT
        ):
        raise HTTPException(status_code=403, detail='Access denied')

    participant = await participants.get(
        conn,
        user_id = user.id,
        direction_id = data.direction_id,
        schema_to_select=Participant,
        return_as_model=True
    )

    if not participant:
        raise HTTPException(status_code=400, detail='Участник не найден')

    if await evaluations.exists(
        conn,
        direction_id = data.direction_id,
        task_id = data.task_id,
        user_id = user.id
    ):
        raise HTTPException(status_code=409, detail='Оценка с такими параметрами уже существует')

    if not await directions.exists(conn, id = participant.direction_id):
        raise HTTPException(status_code=404, detail='Направление с предоставленным id не найдено')

    task: Task | None = await tasks.get(
        conn,
        id = data.task_id,
        schema_to_select=Task,
        return_as_model=True
    )

    if not task:
        raise HTTPException(status_code=404, detail='Задача с предоставленным id не найдена')

    if task.max_score < data.score:
        raise HTTPException(status_code=400, detail='Оценка не может быть больше максимальной')
    
    if not await users.exists(conn, id = user.id):
        raise HTTPException(status_code=404, detail='Пользователь с предоставленным id не найден')

    return await evaluations.create(
        db=conn,
        object=EvaluationCreate(**(data.model_dump()))
    )
