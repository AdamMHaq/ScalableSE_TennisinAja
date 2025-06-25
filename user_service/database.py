from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
from mock_data import MOCK_USERS
import os
import asyncio

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = "tennisinaja"

client = AsyncIOMotorClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
db = client[DB_NAME]

user_collection: Collection = db["users"]

async def wait_for_mongodb():
    """Wait for MongoDB to be ready"""
    max_retries = 30
    for i in range(max_retries):
        try:
            await client.admin.command('ping')
            print("MongoDB connection successful")
            return True
        except Exception as e:
            print(f"MongoDB not ready (attempt {i+1}/{max_retries}): {e}")
            await asyncio.sleep(1)
    return False

async def setup_database():
    """Setup database and insert mock data if needed"""
    try:
        if not await wait_for_mongodb():
            print("Failed to connect to MongoDB")
            return
            
        # Insert mock data if collection is empty
        await insert_mock_data()
        
    except Exception as e:
        print(f"Error setting up database: {e}")

async def insert_mock_data():
    """Insert mock user data if the collection is empty"""
    try:
        # Check if collection is empty
        count = await user_collection.count_documents({})
        if count == 0:
            print("Inserting mock user data...")
            await user_collection.insert_many(MOCK_USERS)
            print(f"Successfully inserted {len(MOCK_USERS)} mock users")
        else:
            print(f"Collection already has {count} users, skipping mock data insertion")
    except Exception as e:
        print(f"Error inserting mock data: {e}")
