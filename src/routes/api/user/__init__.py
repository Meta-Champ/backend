from fastapi import APIRouter
from .get import router as get_router
from .dump import router as dump_router
from .update import router as update_router
from .fill_profile import router as fill_profile_router


router = APIRouter(
    prefix='/user',
    tags=['Пользователи']
)

router.include_router(get_router)
router.include_router(dump_router)
router.include_router(update_router)
router.include_router(fill_profile_router)
