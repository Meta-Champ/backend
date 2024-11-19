from src.core.database import get_async_session
from src.core.schema import (
    Task as TaskSchema,
    Direction as DirectionSchema
)
from src.middlewares import authenticate
from src.models.task import Task, TaskCreate
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __400__, __403__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
tasks = FastCRUD(TaskSchema)
directions = FastCRUD(DirectionSchema)


@router.post(
    path='/',
    response_model=Task,
    responses={
        400: __400__,
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Создание задачи',
    response_description='Задача создана',
)
async def request(
    data: TaskCreate,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Task | HTTPException:
    if not await directions.exists(conn, id = data.direction_id):
        raise HTTPException(status_code=400, detail='Направление не найдено')

    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN]:
        raise HTTPException(status_code=403, detail='Access denied')

    return await tasks.create(
        db=conn,
        object=TaskCreate(**(data.model_dump()))
    )
