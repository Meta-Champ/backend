from fastapi import APIRouter
# from . import router as _router


router = APIRouter(
    prefix='/direction',
    tags=['Направления']
)

# router.include_router(_router)

