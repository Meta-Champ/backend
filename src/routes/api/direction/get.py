from src.core.database import get_async_session
from src.core.schema import Direction as DirectionSchema
from src.middlewares import authenticate
from src.models.direction import Direction
from src.utils.documentation_statuses import __403__, __404__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
directions = FastCRUD(DirectionSchema)


@router.get(
    path='/{id}',
    response_model=Direction,
    responses={
        403: __403__,
        404: __404__,
        500: __500__,
    },
    status_code=200,
    summary='Получение направления',
    response_description='Направление получено',
)
async def request(
    id: int,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Direction | HTTPException:
    row: Direction | None = await directions.get(
        conn,
        id=id,
        schema_to_select=Direction,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Направление не найдено')

    return row
