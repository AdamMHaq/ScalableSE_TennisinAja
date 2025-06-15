from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from database import get_database

router = APIRouter()

async def get_collection():
    db = await get_database()
    return db.bookings

@router.get("/")
async def get_bookings(collection: AsyncIOMotorCollection = Depends(get_collection)):
    try:
        bookings = await collection.find().to_list(1000)
        return bookings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_booking(booking: dict, collection: AsyncIOMotorCollection = Depends(get_collection)):
    try:
        result = await collection.insert_one(booking)
        if result.inserted_id:
            return {"message": "Booking created successfully", "booking_id": str(result.inserted_id)}
        raise HTTPException(status_code=400, detail="Failed to create booking")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))