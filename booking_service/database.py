from motor.motor_asyncio import AsyncIOMotorClient
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