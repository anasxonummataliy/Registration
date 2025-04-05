from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.auth import router as auth_router
from app.database.base import Base 
from app.database.session import async_engine
import app.database.models.users

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()

app = FastAPI(
    title="Auth API",
    description="Auth API",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(auth_router)