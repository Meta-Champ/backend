from fastapi import APIRouter
# from . import router as _router


router = APIRouter(
    prefix='/user',
    tags=['Пользователи']
)

# router.include_router(_router)

