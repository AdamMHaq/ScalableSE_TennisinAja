from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from database import get_database

router = APIRouter()

async def get_collection():
    db = await get_database()
    return db.courts

@router.get("/")
async def get_courts(collection: AsyncIOMotorCollection = Depends(get_collection)):
    try:
        courts = await collection.find().to_list(1000)
        return courts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{court_id}")
async def get_court(court_id: str, collection: AsyncIOMotorCollection = Depends(get_collection)):
    try:
        court = await collection.find_one({"_id": court_id})
        if court is None:
            raise HTTPException(status_code=404, detail="Court not found")
        return court
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))