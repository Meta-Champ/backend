from src.core.database import get_async_session
from src.core.schema import Protocol as ProtocolSchema
from src.middlewares import authenticate
from src.models.protocol import Protocol
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __400__, __403__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
protocols = FastCRUD(ProtocolSchema)


@router.delete(
    path='/{id}',
    response_model=Protocol,
    responses={
        400: __400__,
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Удаление протокола',
    response_description='Протокол удален',
)
async def request(
    id: int,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Protocol | HTTPException:
    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN]:
        raise HTTPException(status_code=403, detail='Access denied')

    row: Protocol | None = await protocols.get(
        conn,
        id = id,
        schema_to_select=Protocol,
        return_as_model=True
    )

    if not row:
        raise HTTPException(status_code=404, detail='Протокол не найден')

    await protocols.delete(db=conn, id=id)

    return row
