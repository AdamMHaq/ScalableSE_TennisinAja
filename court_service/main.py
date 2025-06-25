from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import courts
from database import setup_indexes
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_indexes()
    yield

app = FastAPI(
    title="TennisinAja - Court Service",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(courts.router, prefix="/courts", tags=["Courts"])

@app.get("/")
def root():
    return {"message": "Welcome to TennisinAja Court Service"}