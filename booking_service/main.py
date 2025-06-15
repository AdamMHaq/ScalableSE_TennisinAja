from fastapi import FastAPI
<<<<<<< HEAD
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from routers import bookings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
=======
from routers import bookings
>>>>>>> 28f03f80133b0d0ad90b22b8bd53cc17c66e20f4

app = FastAPI(
    title="TennisinAja - Booking Service",
    version="1.0.0"
)

<<<<<<< HEAD
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient("mongodb://mongo:27017")
    app.mongodb = app.mongodb_client.tennisinaja
    try:
        await app.mongodb_client.server_info()
        logger.info("Connected to MongoDB successfully!")
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
    logger.info("MongoDB connection closed")

app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])

@app.get("/")
async def root():
=======
app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])

@app.get("/")
def root():
>>>>>>> 28f03f80133b0d0ad90b22b8bd53cc17c66e20f4
    return {"message": "Welcome to TennisinAja Booking Service"}