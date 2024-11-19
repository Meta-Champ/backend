from fastapi import APIRouter
# from . import router as _router


router = APIRouter(
    prefix='/evaluation',
    tags=['Оценка']
)

# router.include_router(_router)

