from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users
from database import setup_database

app = FastAPI(
    title="TennisinAja - User Service",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await setup_database()

app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Welcome to TennisinAja User Service"}
