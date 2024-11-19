from fastapi import APIRouter
# from . import router as _router


router = APIRouter(
    prefix='/delivery',
    tags=['Доставка']
)

# router.include_router(_router)

