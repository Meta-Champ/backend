from fastapi import APIRouter
# from .add import router as add_router
# from .dump import router as dump_router
# from .get import router as get_router
# from .update import router as update_router
# from .delete import router as delete_router


router = APIRouter(
    prefix='/person',
    tags=['Персоны']
)

# router.include_router(add_router)
# router.include_router(dump_router)
# router.include_router(get_router)
# router.include_router(update_router)
# router.include_router(delete_router)

