from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import *
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio.session import Session

sync_engine = create_engine(DB_SETTINGS.sync_url, echo=False)
async_engine = create_async_engine(DB_SETTINGS.sync_url, echo=False)

class Base(DeclarativeBase):
    pass

async_sess_maker = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False
)

sync_sess_maker = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False
)

async def get_sess():
    async with async_sess_maker() as sess:
        yield sess

def get_sync_sess():
    with sync_sess_maker() as sess:
        yield sess

SessionDep = Annotated[AsyncSession, Depends(get_sess)]
SyncSessionDep = Annotated[Session, Depends(get_sync_sess)]