from src.core.settings import settings
from src.core.setup import create_application
from src.routes import router
from loguru import logger
import uvicorn, sys

logger.remove(0)
logger.add(sys.stdout, level=settings.server.LOG_LEVEL.upper())
logger.add('logs/latest.log', rotation="1 GB")

application = create_application(router=router, settings=settings)

def main():
    uvicorn.run(
        application,
        host=settings.server.HOST,
        port=settings.server.PORT,
        log_level=settings.server.LOG_LEVEL
    )

if __name__ == '__main__':
    main()
