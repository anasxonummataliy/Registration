from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.regis import router as regis_router
from app.database.base import create_db_and_tables

@asynccontextmanager
async def lifespan(app : FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(
    title="Regis Api",
    description="Regis Api",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend domeni
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(regis_router)