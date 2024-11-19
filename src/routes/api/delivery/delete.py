from src.core.database import get_async_session
from src.core.schema import Delivery as DeliverySchema
from src.middlewares import authenticate
from src.models.delivery import Delivery
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __400__, __403__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
deliveries = FastCRUD(DeliverySchema)


@router.delete(
    path='/{id}',
    response_model=Delivery,
    responses={
        400: __400__,
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Удаление доставки',
    response_description='Доставка удалена',
)
async def request(
    id: int,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Delivery | HTTPException:
    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN]:
        raise HTTPException(status_code=403, detail='Access denied')

    row: Delivery | None = await deliveries.get(
        conn,
        id = id,
        schema_to_select=Delivery,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Доставка не найдена')

    await deliveries.delete(db=conn, id=id)

    return row
