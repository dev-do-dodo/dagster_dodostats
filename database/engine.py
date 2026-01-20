from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config import Config, load_config

cfg: Config = load_config()
engine = create_async_engine(f'postgresql+asyncpg://'
                             f'{cfg.db.user}:'
                             f'{cfg.db.password}@'
                             f'{cfg.db.host}:'
                             f'5432/'
                             f'{cfg.db.name}')

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
