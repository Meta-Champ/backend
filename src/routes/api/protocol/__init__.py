from fastapi import APIRouter
# from . import router as _router


router = APIRouter(
    prefix='/protocol',
    tags=['Протоколы']
)

# router.include_router(_router)

