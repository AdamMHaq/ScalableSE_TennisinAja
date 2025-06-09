from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = "tennisinaja"

client = AsyncIOMotorClient(MONGODB_URL)
db = client[DB_NAME]
booking_collection = db["bookings"]