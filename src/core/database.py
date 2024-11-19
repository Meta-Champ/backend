from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from .settings import settings

formatted_link = f"postgresql+asyncpg://{settings.database.USER}:{settings.database.PASS}@" + \
    f"{settings.database.HOST}:{settings.database.PORT}/{settings.database.BASE}"

async_engine  = create_async_engine(formatted_link, echo=False, future=True)
async_session_maker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
