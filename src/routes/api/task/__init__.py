from fastapi import APIRouter
# from . import router as _router


router = APIRouter(
    prefix='/task',
    tags=['Задачи']
)

# router.include_router(_router)

