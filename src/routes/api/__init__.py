from fastapi import APIRouter
from .auth import router as auth_router
from .championship import router as championship_router
from .delivery import router as delivery_router
from .direction import router as direction_router
from .evaluation import router as evaluation_router
from .participant import router as participant_router
from .person import router as person_router
from .protocol import router as protocol_router
from .task import router as task_router
from .user import router as user_router


router = APIRouter()
router.include_router(auth_router)
router.include_router(championship_router)
router.include_router(delivery_router)
router.include_router(direction_router)
router.include_router(evaluation_router)
router.include_router(participant_router)
router.include_router(person_router)
router.include_router(protocol_router)
router.include_router(task_router)
router.include_router(user_router)
