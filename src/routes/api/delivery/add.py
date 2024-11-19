from src.core.database import get_async_session
from src.core.schema import (
    Delivery as DeliverySchema,
    Direction as DirectionSchema,
    Participant as ParticipantSchema
)
from src.middlewares import authenticate
from src.models.delivery import Delivery, DeliveryCreate
from src.models.participant import Participant
from src.models.role import SystemRoles, DirectionRoles
from src.utils.documentation_statuses import __400__, __403__, __500__

from fastapi import APIRouter, Depends, HTTPException
from fastcrud import FastCRUD

router = APIRouter()
deliveries = FastCRUD(DeliverySchema)
directions = FastCRUD(DirectionSchema)
participants = FastCRUD(ParticipantSchema)


@router.post(
    path='/',
    response_model=Delivery,
    responses={
        400: __400__,
        403: __403__,
        500: __500__,
    },
    status_code=200,
    summary='Создание доставки',
    response_description='Доставка создана',
)
async def request(
    data: DeliveryCreate,
    user = Depends(authenticate.check),
    conn = Depends(get_async_session)
) -> Delivery | HTTPException:
    if not await directions.exists(conn, id = data.direction_id):
        raise HTTPException(status_code=400, detail='Направление не найдено')

    participant: bool = await participants.get(
        conn,
        id = user.id,
        direction_id = data.direction_id,
        schema_to_select=Participant,
        return_as_model=True
    )

    if user.role not in [SystemRoles.OWNER, SystemRoles.ADMIN] or \
        participant and participant.role not in [DirectionRoles.CHIEF_EXPERT, DirectionRoles.TECHNICAL_ADMINISTRATOR]:
        raise HTTPException(status_code=403, detail='Access denied')

    return await deliveries.create(
        db=conn,
        object=DeliveryCreate(**(data.model_dump()))
    )
