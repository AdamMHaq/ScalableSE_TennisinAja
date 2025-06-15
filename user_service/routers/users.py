from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from database import get_database

router = APIRouter()

async def get_collection():
    db = await get_database()
    return db.users

@router.get("/")
async def get_users(collection: AsyncIOMotorCollection = Depends(get_collection)):
    try:
        users = await collection.find().to_list(1000)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
async def get_user(user_id: str, collection: AsyncIOMotorCollection = Depends(get_collection)):
    try:
        user = await collection.find_one({"_id": user_id})
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))