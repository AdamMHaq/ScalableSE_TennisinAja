from motor.motor_asyncio import AsyncIOMotorClient
<<<<<<< HEAD
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def connect_to_mongo():
    try:
        client = AsyncIOMotorClient("mongodb://mongo:27017", serverSelectionTimeoutMS=5000)
        await client.server_info()
        logger.info("Connected to MongoDB successfully!")
        db = client.tennisinaja
        return db
    except (ConfigurationError, ServerSelectionTimeoutError) as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        raise

async def get_database():
    return await connect_to_mongo()
=======
import os

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = "tennisinaja"

client = AsyncIOMotorClient(MONGODB_URL)
db = client[DB_NAME]
booking_collection = db["bookings"]
>>>>>>> 28f03f80133b0d0ad90b22b8bd53cc17c66e20f4
