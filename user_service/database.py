from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
import os

# MongoDB connection URI (adjust if needed)
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = "tennisinaja"

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGODB_URL)
db = client[DB_NAME]

# Reference to your users collection
user_collection: Collection = db["users"]
