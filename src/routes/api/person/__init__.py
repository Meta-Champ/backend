from fastapi import APIRouter
# from . import router as _router


router = APIRouter(
    prefix='/person',
    tags=['Персоны']
)

# router.include_router(_router)

