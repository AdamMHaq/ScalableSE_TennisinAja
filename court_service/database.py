from motor.motor_asyncio import AsyncIOMotorClient
from schema import COURT_INDEXES
from mock_data import MOCK_COURTS
import os
import asyncio

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = "tennisinaja_courts"

client = AsyncIOMotorClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
db = client[DB_NAME]
court_collection = db["courts"]

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

async def setup_indexes():
    """Setup database indexes for better query performance"""
    try:
        if not await wait_for_mongodb():
            print("Failed to connect to MongoDB")
            return
            
        await court_collection.create_indexes(COURT_INDEXES)
        print("Database indexes created successfully")
        
        # Insert mock data if collection is empty
        await insert_mock_data()
        
    except Exception as e:
        print(f"Error creating indexes: {e}")

async def insert_mock_data():
    """Insert mock court data if the collection is empty"""
    try:
        print(f"MOCK_COURTS has {len(MOCK_COURTS)} items")
        await court_collection.delete_many({})
        result = await court_collection.insert_many(MOCK_COURTS)
        print(f"Inserted court IDs: {result.inserted_ids}")
    except Exception as e:
        print(f"Error inserting mock data: {e}")
