from src.core.database import get_async_session
from src.core.schema import Direction as DirectionSchema
from src.middlewares import authenticate
from src.models.direction import Direction, DirectionUpdate
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __400__, __403__, __404__, __409__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
directions = FastCRUD(DirectionSchema)


@router.patch(
    path='/{id}',
    response_model=Direction,
    responses={
        400: __400__,
        403: __403__,
        404: __404__,
        409: __409__,
        500: __500__,
    },
    status_code=200,
    summary='Обновление направления',
    response_description='Направление обновлено',
)
async def request(
    id: int, 
    data: DirectionUpdate,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Direction | HTTPException:
    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN]:
        raise HTTPException(status_code=403, detail='Access denied')

    row: Direction | None = await directions.get(
        conn,
        id = id,
        schema_to_select=Direction,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Направление не найдено')

    exist: Direction | None = await directions.get(
        conn,
        name = data.name,
        schema_to_select=Direction,
        return_as_model=True
    )

    if exist and exist.id != id:
        raise HTTPException(status_code=400, detail='Направление с таким названием уже существует')

    obj = {}

    if data.name is not None:
        obj[DirectionSchema.name.name] = data.name

    if data.is_juniors is not None:
        obj[DirectionSchema.is_juniors.name] = data.is_juniors

    conflict: Direction | None = await directions.get(
        conn,
        name = obj[DirectionSchema.name.name] if DirectionSchema.name.name in obj else data.name,
        is_juniors = obj[DirectionSchema.is_juniors.name] if DirectionSchema.is_juniors.name in obj else data.is_juniors,
        schema_to_select=Direction,
        return_as_model=True
    )

    if conflict and conflict.id != id:
        raise HTTPException(status_code=409, detail='Направление с такими параметрами уже существует')

    await directions.update(db=conn, id=id, object=obj)

    return Direction(**{**row, **obj})
