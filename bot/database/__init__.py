from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings

engine = create_async_engine(url=settings.POSTGRES_URL_asyncpg, echo=settings.DEBUG)

session = async_sessionmaker(engine)
