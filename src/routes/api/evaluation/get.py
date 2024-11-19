from src.core.database import get_async_session
from src.core.schema import Evaluation as EvaluationSchema
from src.middlewares import authenticate
from src.models.evaluation import Evaluation
from src.utils.documentation_statuses import __403__, __404__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
evaluations = FastCRUD(EvaluationSchema)


@router.get(
    path='/{id}',
    response_model=Evaluation,
    responses={
        403: __403__,
        404: __404__,
        500: __500__,
    },
    status_code=200,
    summary='Получение оценки',
    response_description='Оценка получена',
)
async def request(
    id: int,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Evaluation | HTTPException:
    row: Evaluation | None = await evaluations.get(
        conn,
        id=id,
        schema_to_select=Evaluation,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Оценка не найдена')

    return row
