from src.core.database import get_async_session
from src.core.schema import Protocol as ProtocolSchema
from src.middlewares import authenticate
from src.models.protocol import Protocol, ProtocolUpdate, ProtocolStatus
from src.models.role import SystemRoles
from src.utils.documentation_statuses import __400__, __403__, __404__, __409__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
protocols = FastCRUD(ProtocolSchema)


@router.patch(
    path='/{id}',
    response_model=Protocol,
    responses={
        400: __400__,
        403: __403__,
        404: __404__,
        500: __500__,
    },
    status_code=200,
    summary='Обновление протокола',
    response_description='Протокол обновлен',
)
async def request(
    id: int, 
    data: ProtocolUpdate,
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

    if row.status not in [ProtocolStatus.PUBLISHED, ProtocolStatus.ASSIGNED]:
        raise HTTPException(status_code=400, detail='Изменение статуса протокола закрыто')

    await protocols.update(db=conn, id=id, object=data)

    return Protocol(**{**row.model_dump(), **data.model_dump()})
