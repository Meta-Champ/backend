from fastapi import APIRouter
# from . import router as _router


router = APIRouter(
    prefix='/participant',
    tags=['Участники']
)

# router.include_router(_router)

